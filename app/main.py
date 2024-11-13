from dotenv import load_dotenv
import os
from fastapi import Body, Depends, FastAPI, HTTPException, status
from starlette.requests import Request
from .models.models import Base, DataReading, Device, DeviceData, Station, UserStation, User
from .models.REST.Token import Token
from .models.REST.AuthParams import AuthParams
from .database import SessionLocal, engine
from datetime import datetime, timedelta, timezone
from .filter_params import FilterParams
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, any_, desc
from typing import Annotated
from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.responses import Response

load_dotenv()
Base.metadata.create_all(bind=engine)


app = FastAPI()
db = SessionLocal()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    # print('plain_password : ' +plain_password)
    # print('hashed_password : ' +hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(user_login: str, password: str):
    user = None
    if len(user_login.split('@')) == 2:
        user = db.query(User).filter(User.email == user_login).first()
    else:
        user = db.query(User).filter(User.username == user_login).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm= os.getenv("ALGORITHM"))
    return encoded_jwt

# =================================================================================================
#
#
#
#
#
#
# =================================================================================================

@app.post("/api/device_push/{device_type}")
async def store_record(device_type: str, request: Request):
    try:
        req_body_bytes = await request.body()
        req_body_str = req_body_bytes.decode('utf-8')
        print("Request body : " + req_body_str)
        req_body_str = req_body_str.replace("\\r", "").replace("\\n", "")
        if req_body_str == '':
            raise HTTPException(400, "E:10")
        data_array = req_body_str.split(",")
        if len(data_array) <= 1:
            raise HTTPException(400, "E:10")
        if len(data_array[9:-1]) != int(data_array[1]):
            raise HTTPException(400, "E:11")

        device = db.query(Device).filter(Device.id == data_array[7]).first()
        if not device:
            raise HTTPException(400, "E:12")
        
        year_val = int(f'20{data_array[2][0]}{data_array[2][1]}')
        month_val = int(f'{data_array[2][2]}{data_array[2][3]}')
        day_val = int(f'{data_array[2][4]}{data_array[2][5]}')
        hour_val = int(f'{data_array[3][0]}{data_array[3][1]}')
        minute_val = int(f'{data_array[3][2]}{data_array[3][3]}')
        date_time = datetime(year=year_val, month=month_val, day=day_val, hour=hour_val, minute=minute_val,
                             second=0)

        device_data = DeviceData(date = date_time, data_length = data_array[1], device_id = data_array[7], ttl = data_array[8],
                                        record_version = data_array[4])

        db.add(device_data)
        for reading in data_array[9:-1]:
            device_reading = DataReading(device_data = device_data, value = int(reading))
            db.add(device_reading)

        db.commit()
        db.refresh(device_data)
        
        return Response(status_code=200, content=f"\"Success {device_type}\"\r\n")
    except IntegrityError as dataInteg:
        print("Data Integrity Exception : " +str(dataInteg))
        db.rollback()
        raise HTTPException(status_code=400, detail="Data integrity error occurred.")
    except SQLAlchemyError as sqlEx:
        print("SQL Exception : " +str(sqlEx))
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as ex:
        db.rollback()
        print("Exception : ", ex)
        return Response(status_code=ex.status_code, content=f"\"{ex.detail}\"\r\n")

@app.post("/api/filter")
async def filter_records(data: FilterParams = Body(...)):
    try:
        if data.page < 1 or data.items_per_page < 0:
            raise HTTPException(status_code=400, detail="Invalid request.")
        
        query = db.query(DeviceData).join(DataReading).filter(and_(DeviceData.date >= data.start_date.date(), DeviceData.date < data.end_date.date() + timedelta(days=1)))

        if data.device_id:
            query = query.filter((DeviceData.device_id == data.device_id))

        if data.operator_id:
            query = query.filter((DataReading.value == data.operator_id))
        
        if data.vehicle_no:
            query = query.filter((DataReading.value == data.vehicle_no))

        device_data = query.options(
            joinedload(DeviceData.device).joinedload(Device.station)).options(
            joinedload(DeviceData.device).joinedload(Device.device_type)).options(
            joinedload(DeviceData.data_readings)).order_by(desc(DeviceData.date)).all()
        
        if data.operator_id:
            device_data = [rec for rec in device_data if rec.data_readings[0].value == data.operator_id]
        
        if data.vehicle_no:
            device_data = [rec for rec in device_data if rec.data_readings[1].value == data.vehicle_no]
        
        res = device_data
        skip = ((data.page) - 1) * data.items_per_page
        res = res[skip : skip + data.items_per_page]

        resp = {
            "total": len(device_data),
            "page": data.page,
            "count": len(res),
            "data": jsonable_encoder(res)
        }

        return JSONResponse(content = resp)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Data integrity error occurred.")
    except SQLAlchemyError as excep:
        print("Excep : " +str(excep))
        raise HTTPException(status_code=500, detail="Database error occurred.")
    except Exception as ex:
        print("Ex : " +str(ex))
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)


@app.get("/api/user-details")
async def get_user_details(token: str = Depends(oauth2_scheme)) -> Token:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,  os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == payload.get("email")).first()
        # token_data = TokenData(username=username)
        if user.user_stations:
            stations = [ob.station for ob in user.user_stations]
        elif user.user_type_id == 1:
            stations = db.query(Station).all()
        resp = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_active": user.is_active,
            "user_type_id": user.user_type_id,
            "stations": jsonable_encoder(stations)
        }
        return JSONResponse(content=resp)
            # "data": jsonable_encoder(user)
    except InvalidTokenError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    # return user


@app.post("/api/token")
async def login_for_access_token(
    req: AuthParams = Body(...),
) -> Token:
    user = authenticate_user(req.user_login, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    access_token = create_access_token(
        data={
            "sub": user.username,
            "email": user.email,
            "role": user.user_type_id
            }, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
# import bcrypt

# # Password to hash
# password = b"passwd123"

# # Generate salt and hash the password
# salt = bcrypt.gensalt(rounds=12)  # You can change the rounds (cost factor) here

# # Hash the password
# hashed_password = bcrypt.hashpw(password, salt)

# # Print the hashed password
# print(f"Hashed Password: {hashed_password.decode()}")
# print(f"Hashed Password: {hashed_password}")

# # Verify the password
# if bcrypt.checkpw(password, hashed_password):
#     print("Password verified successfully!")
# else:
#     print("Password verification failed!")


import bcrypt
import pymysql

# Connect to MySQL database (use your database connection details)
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="passwd123",
    database="test-db"
)

cursor = conn.cursor()

# Get the hashed password for the user 'usama.latif' from the database
cursor.execute("SELECT password FROM users WHERE username = 'usama.latif'")
stored_hash = cursor.fetchone()

if stored_hash:
    stored_hash = stored_hash[0]  # Extract the hashed password from the tuple

    # The password entered by the user
    input_password = "passwd123"  # Example user input (should be dynamic in production)

    # Verify the entered password with the stored hash
    if bcrypt.checkpw(input_password.encode('utf-8'), stored_hash.encode('utf-8')):
        print("Password is correct!")
    else:
        print("Password is incorrect!")
else:
    print("User not found.")

# Close the database connection
cursor.close()
conn.close()

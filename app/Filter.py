class Filter:
    """
    Represents a filter for records based on start date, end date, and device ID.
    """

    def __init__(self, start_date: Optional[str] = None, end_date: Optional[str] = None, device_id: Optional[int] = None):
        self.start_date = start_date
        self.end_date = end_date
        self.device_id = device_id

    # @staticmethod
    # def from_query(query: Query) -> Filter:
    #     """
    #     Creates a Filter instance from a FastAPI query object.
    #     """
    #     return Filter(
    #         start_date=query.get("start_date"),
    #         end_date=query.get("end_date"),
    #         device_id=query.get("device_id")
    #     )

    def __str__(self) -> str:
        """
        Returns a string representation of the filter.
        """
        return f"Filter(start_date={self.start_date}, end_date={self.end_date}, device_id={self.device_id})"
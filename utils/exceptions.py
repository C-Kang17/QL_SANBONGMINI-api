class CustomException(Exception):
    def __init__(self, type: str, status: int, title: str, detail: str):
        self.type = type
        self.status = status
        self.title = title
        self.detail = detail

    def __str__(self):
        return f"{self.title}: {self.detail}"

class ErrorCode:
    @staticmethod
    def InvalidDate(date: str):
        return CustomException(
            type="core/info/invalid-date", status=400, title="Invalid date format.", detail=f"The {date} is not a valid date. Please provide a valid date with YYYY-MM-DD format and try again."
        )

    @staticmethod
    def InvalidDateTime(date: str):
        return CustomException(
            type="core/info/invalid-date-time",
            status=400,
            title="Invalid date time format.",
            detail=f"The {date} is not a valid date time. Please provide a valid date time with YYYY-MM-DD HH:MM:SS format and try again.",
        )
    
    @staticmethod
    def InvalidTime(time: str):
        return CustomException(
            type="core/info/invalid-time",
            status=400,
            title="Invalid Time Format",
            detail=f"The time '{time}' is not valid. Please provide a valid time in the format 'HH:MM:SS'."
        )
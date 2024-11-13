from datetime import datetime, timedelta
from typing import Annotated
from pydantic.functional_validators import AfterValidator
from fastapi import HTTPException

from .exceptions import ErrorCode as CoreErrorCode

def check_date_format(value: str) -> str:
    """
    Validates whether a given string matches the date format "%Y-%m-%d".

    Args:
        value (str): The string to validate as a date.

    Returns:
        str: The validated date string.

    Raises:
        CoreErrorCode.InvalidDate: If the string does not match the date format "%Y-%m-%d".

    """
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise CoreErrorCode.InvalidDate(date=value)

def check_datetime_str(value: str) -> str:
    """
    Validates whether a given string matches the datetime format "%Y-%m-%d %H:%M:%S".

    Args:
        value (str): The string to validate as a datetime.

    Returns:
        str: The validated datetime string.

    Raises:
        CoreErrorCode.InvalidDate: If the string does not match the datetime format "%Y-%m-%d %H:%M:%S".
    """
    try:
        datetime.strptime(value, "%H:%M:%S")
        return value
    except ValueError:
        raise CoreErrorCode.InvalidDateTime(date=value)


DateStr = Annotated[str, AfterValidator(check_date_format)]
TimeStr = Annotated[str, AfterValidator(check_datetime_str)]
from datetime import datetime
from app.core.settings import logger


def format_date(date_str):
    try:
        if isinstance(date_str, datetime):
            return date_str.strftime("%Y-%m-%d")
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%Y-%m-%d")
    except ValueError as e:
        logger.error(f"Error parsing date string '{date_str}': {e}")
        return date_str

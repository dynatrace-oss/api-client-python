import warnings
import functools
from datetime import datetime
from typing import Union, Optional

ISO_8601 = "%Y-%m-%dT%H:%M:%S.%fZ"


def deprecated(reason=""):
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            warnings.warn(f"'{func.__name__}' is deprecated. {reason}", category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return new_func

    return decorator


def timestamp_to_string(timestamp: Optional[Union[datetime, str]]) -> Optional[str]:
    if not isinstance(timestamp, datetime):
        return timestamp
    return timestamp.isoformat(timespec="milliseconds")


def iso8601_to_datetime(timestamp: Optional[str]) -> Optional[datetime]:
    if isinstance(timestamp, str):
        return datetime.strptime(timestamp, ISO_8601)
    return timestamp

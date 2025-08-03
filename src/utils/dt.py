from datetime import datetime
from datetime import timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

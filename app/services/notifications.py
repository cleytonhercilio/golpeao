from datetime import datetime, timezone
from typing import List

_feed: List[dict] = []
_MAX_SIZE = 100


def add_event(event_type: str, message: str, user_display: str = None, icon: str = "⚽") -> None:
    _feed.insert(0, {
        "type": event_type,
        "message": message,
        "user": user_display,
        "icon": icon,
        "at": datetime.now(timezone.utc).isoformat(),
    })
    if len(_feed) > _MAX_SIZE:
        _feed.pop()


def get_feed(limit: int = 20) -> List[dict]:
    return _feed[:limit]

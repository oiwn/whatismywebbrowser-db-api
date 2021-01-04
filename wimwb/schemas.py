from datetime import datetime

from pydantic import BaseModel


class UserAgentShort(BaseModel):
    """Define minimal required useragent record"""
    id: int
    user_agent: str
    times_seen: int
    first_seen_at: datetime
    updated_at: datetime

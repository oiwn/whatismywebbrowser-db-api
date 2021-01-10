from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserAgentShort(BaseModel):
    """Define minimal required useragent record"""
    user_agent: str
    times_seen: int
    first_seen_at: datetime
    operating_system_name_code: str
    software_name: str
    updated_at: Optional[datetime]  # pylint: disable=unsubscriptable-object

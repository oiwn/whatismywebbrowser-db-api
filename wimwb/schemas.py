# pylint: disable=unsubscriptable-object
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class UserAgentShort(BaseModel):
    """Define minimal required useragent record"""

    user_agent: str
    times_seen: int
    first_seen_at: datetime
    operating_system_name_code: Optional[str]
    software_name: Optional[str]
    updated_at: Optional[datetime]  # pylint: disable=unsubscriptable-object

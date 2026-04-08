from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    email_id: int
    subject: str
    body: str
    sender: str
    priority: str
    attachments: bool
    thread_id: str

    # memory / history
    history: List[str]

class Action(BaseModel):
    action_type: str  # reply, ignore, escalate, classify, mark_spam, mark_important
    content: Optional[str] = None

class Reward(BaseModel):
    value: float
    reason: str
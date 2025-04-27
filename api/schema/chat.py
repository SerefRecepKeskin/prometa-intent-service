from typing import AnyStr, List
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    message: str


class ConversationRequest(BaseModel):
    messages: List[Message]
    session_identifier: UUID


class AnalysisItem(BaseModel):
    role: str
    sentence: str
    sentiment: str
    intent: str


class MessageResult(BaseModel):
    bot_message: AnyStr
    session_id: UUID
    analysis: List[AnalysisItem] = []

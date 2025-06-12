from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime

class ChatMessageBase(BaseModel):
    content: str
    is_bot: bool = False
    metadata: Optional[Dict[str, Any]] = None

class ChatMessageCreate(ChatMessageBase):
    session_id: int

class ChatMessage(ChatMessageBase):
    id: int
    session_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    session_name: Optional[str] = "New Chat"

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSession(ChatSessionBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    messages: List[ChatMessage] = []

    class Config:
        from_attributes = True

class ChatQuery(BaseModel):
    message: str
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    message: str
    products: List[Dict[str, Any]] = []
    session_id: int
    is_bot: bool = True

class MessageBase(BaseModel):
    content: str
    is_user: bool = True

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ChatSessionBase(BaseModel):
    user_id: int

class ChatSessionCreate(ChatSessionBase):
    pass

class ChatSessionResponse(ChatSessionBase):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

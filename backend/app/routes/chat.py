from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.user import User
from ..models.chat import ChatSession, ChatMessage
from ..schemas.chat import (
    ChatQuery, ChatResponse, ChatSession as ChatSessionSchema,
    ChatMessage as ChatMessageSchema
)
from ..services.chatbot import ChatbotService
from .auth import get_current_user
import json

router = APIRouter()

@router.post("/query", response_model=ChatResponse)
def chat_query(
    query: ChatQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process chat query and return response"""
    
    # Get or create chat session
    if query.session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == query.session_id,
            ChatSession.user_id == current_user.id
        ).first()
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
    else:
        # Create new session
        session = ChatSession(user_id=current_user.id)
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # Save user message
    user_message = ChatMessage(
        session_id=session.id,
        content=query.message,
        is_bot=False
    )
    db.add(user_message)
    
    # Process with chatbot service
    chatbot = ChatbotService(db)
    bot_response = chatbot.process_message(query.message, current_user.id)
    
    # Save bot response
    bot_message = ChatMessage(
        session_id=session.id,
        content=bot_response['message'],
        is_bot=True,
        metadata=json.dumps({
            'products': bot_response['products'],
            'suggestions': bot_response.get('suggestions', [])
        })
    )
    db.add(bot_message)
    db.commit()
    
    return ChatResponse(
        message=bot_response['message'],
        products=bot_response['products'],
        session_id=session.id,
        suggestions=bot_response.get('suggestions', [])
    )

@router.get("/sessions", response_model=List[ChatSessionSchema])
def get_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's chat sessions"""
    sessions = db.query(ChatSession)\
        .filter(ChatSession.user_id == current_user.id)\
        .order_by(ChatSession.updated_at.desc())\
        .all()
    return sessions

@router.get("/sessions/{session_id}", response_model=ChatSessionSchema)
def get_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific chat session with messages"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    return session

@router.delete("/sessions/{session_id}")
def delete_chat_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete chat session"""
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    db.delete(session)
    db.commit()
    
    return {"message": "Chat session deleted successfully"}

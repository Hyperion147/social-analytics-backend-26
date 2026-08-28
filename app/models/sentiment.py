import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class SentimentResult(Base):
    __tablename__ = "sentiment_results"

    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    sentiment = Column(String(32), nullable=False)   # positive, negative, neutral
    emotion = Column(String(32), nullable=False)     # anger, joy, sadness, fear, surprise, sarcasm
    confidence = Column(Float, nullable=False)
    model_version = Column(String(32), default="v1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
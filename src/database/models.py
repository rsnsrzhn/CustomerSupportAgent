from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
import datetime

class Base(DeclarativeBase):
    pass 

class SupportLog(Base):
    __tablename__ = "support_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    message_text = Column(Text)
    ai_answer = Column(Text)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
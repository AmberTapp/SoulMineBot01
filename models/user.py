from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String␊
from sqlalchemy.dialects.postgresql import JSONB␊
␊
from ..config.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String, index=True)
    first_name = Column(String)
    last_name = Column(String)
    language_code = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_interaction = Column(DateTime)
    wallet_address = Column(String)
    verified = Column(Boolean, default=False)
    subscription_status = Column(String, default='free')  # 'free', 'premium'
    subscription_end_date = Column(DateTime)
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(String, ForeignKey("users.id"))
    total_points = Column(Integer, default=0)
    loyalty_level = Column(Integer, default=1)
    notifications_enabled = Column(Boolean, default=True)
    preferences = Column(JSONB, default=dict)
    profile_metadata = Column("metadata", JSONB, default=dict)
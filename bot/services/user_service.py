from sqlalchemy.orm import Session
from models.user import User
from bot.utils.database import get_user_by_telegram_id
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user(self, telegram_id: str) -> User:
        """Get user by Telegram ID"""
        return get_user_by_telegram_id(self.db, telegram_id)
    
    async def create_user(self, telegram_id: str, **kwargs) -> User:
        """Create new user"""
        user = User(
            id=str(uuid.uuid4()),
            telegram_id=telegram_id,
            **kwargs
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def update_user(self, user: User, **kwargs) -> User:
        """Update user information"""
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: str) -> User:
        """Get user by internal ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    async def get_users_by_level(self, level: int) -> list[User]:
        """Get users by loyalty level"""
        return self.db.query(User).filter(User.loyalty_level == level).all()
    
    async def get_total_users(self) -> int:
        """Get total number of users"""
        return self.db.query(User).count()
    
    async def get_active_users(self) -> int:
        """Get number of active users"""
        return self.db.query(User).filter(User.is_active == True).count()
    
    async def get_user_statistics(self) -> dict:
        """Get user statistics"""
        total_users = self.get_total_users()
        active_users = self.get_active_users()
        
        # Get users by level
        users_by_level = {}
        for level in range(1, 6):
            count = self.db.query(User).filter(User.loyalty_level == level).count()
            users_by_level[level] = count
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'users_by_level': users_by_level
        }

# Global service instance
user_service = None

def get_user_service(db: Session) -> UserService:
    global user_service
    if user_service is None:
        user_service = UserService(db)
    return user_service
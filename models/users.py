from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Index
from datetime import datetime

class Base(DeclarativeBase):
    pass
    
class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    user_fullname: Mapped[str] = mapped_column(String(100), nullable=False, default='User')
    referral_link: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    balance: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default=lambda x: str(datetime.now().strftime('%d.%m.%Y, %H:%M:%S'))
    )
    
    __table_args__ = (
        Index('user_id_index', 'user_id'),
    )
    
    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_fullname': self.user_fullname,
            'referral_link': self.referral_link,
            'balance': self.balance,
            'created_at': self.created_at
        }

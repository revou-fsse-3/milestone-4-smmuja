from models.base import Base
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

class Account(Base):
    __tablename__= 'account'

    id = mapped_column(Integer, primary_key = True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    account_type = mapped_column (Enum ('Checking', 'Savings'), nullable=False)
    account_number = mapped_column (String(255), nullable=False)
    balance = mapped_column (DECIMAL(10, 2), nullable=False)
    created_at = mapped_column (DateTime(timezone=True), default=func.now())
    updated_at = mapped_column (DateTime(timezone=True), default=func.now(), nullable=True)

    def __repr__(self):
        return f'<Account {self.id}>'


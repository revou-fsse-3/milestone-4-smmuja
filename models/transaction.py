from models.base import Base
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum, DECIMAL
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

class Transaction(Base):
    __tablename__= 'transaction'

    id = mapped_column(Integer, primary_key = True, autoincrement=True)
    user_id = mapped_column(Integer, ForeignKey("account.id", ondelete="CASCADE"))
    from_account_id = mapped_column (Integer, ForeignKey("account.id", ondelete="CASCADE"))
    to_account_id = mapped_column (Integer, ForeignKey("account.id", ondelete="CASCADE"))
    amount = mapped_column(DECIMAL(10, 2), nullable=False)
    type
    description = mapped_column(Text(255), nullable=True)
    created_at = mapped_column (DateTime(timezone=True), default=func.now())


    def __repr__(self):
        return f'<Transaction {self.id}>'


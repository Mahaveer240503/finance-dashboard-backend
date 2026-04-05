from sqlmodel import SQLModel, Field
from datetime import datetime
from datetime import datetime, timezone
from enum import Enum

from decimal import Decimal

class RoleEnum(str, Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    hashed_password: str  
    role: RoleEnum = Field(default=RoleEnum.viewer)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    
class TransactionType(str, Enum):
    income = "income"
    expense = "expense"

class Record(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: Decimal = Field(max_digits=10, decimal_places=2) # 👈 The Pro move!
    type: TransactionType = Field(index=True)
    category: str = Field(index=True)
    date: datetime = Field(index=True) # Indexed for fast Dashboard filtering
    note: str | None = None
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    is_deleted: bool = Field(default=False) # Soft delete
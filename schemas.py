from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal
from models import RoleEnum, TransactionType

# ==========================
# USER SCHEMAS
# ==========================

class UserCreate(BaseModel):
    """What the user sends us when registering."""
    name: str
    email: EmailStr  # Automatically validates a proper email format!
    password: str    # Raw password (we will hash this in the route)
    role: RoleEnum = RoleEnum.viewer

class UserResponse(BaseModel):
    """What we send back to the user (Notice: NO PASSWORD HERE)."""
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    is_active: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }


# ==========================
# RECORD SCHEMAS
# ==========================

class RecordCreate(BaseModel):
    """What the user sends to create a financial entry."""
    amount: Decimal
    type: TransactionType
    category: str
    date: datetime
    note: str | None = None
    # 💡 Notice: We DO NOT include owner_id here. 
    # The user shouldn't tell us who they are in the JSON body.
    # We will securely extract their ID from their authentication token later!

class RecordResponse(BaseModel):
    """What we send back when they request their records."""
    id: int
    amount: Decimal
    type: TransactionType
    category: str
    date: datetime
    note: str | None = None
    owner_id: int
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }
    
class CategoryTotal(BaseModel):
    category: str
    total: Decimal
    
    model_config = {
        "from_attributes": True
    }
    
    
    
# Add this to the bottom of schemas.py
class DashboardSummary(BaseModel):
    """What we send back for the dashboard analytics."""
    total_income: Decimal
    total_expenses: Decimal
    net_balance: Decimal
    category_totals: list[CategoryTotal]         # 👈 NEW!
    recent_activity: list[RecordResponse]        # 👈 NEW! (Reusing our existing schema)
    
    model_config = {
        "from_attributes": True
    }
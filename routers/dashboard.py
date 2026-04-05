from fastapi import APIRouter, Depends
from sqlmodel import Session, select, desc
from sqlalchemy import func
from decimal import Decimal

from database import get_session
from models import Record, TransactionType, User
from schemas import DashboardSummary, CategoryTotal
from dependencies import require_analyst_or_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    session: Session = Depends(get_session),
    current_user: User = Depends(require_analyst_or_admin) # 🔒 Security check!
):
    """Get aggregated financial data (Analyst & Admin Only)."""

    # 1. Calculate Total Income directly in the database
    income_query = select(func.sum(Record.amount)).where(
        Record.type == TransactionType.income,
        Record.is_deleted == False,
        Record.owner_id == current_user.id
    )
    total_income = session.exec(income_query).scalar() or Decimal("0.00")

    # 2. Calculate Total Expenses directly in the database
    expense_query = select(func.sum(Record.amount)).where(
        Record.type == TransactionType.expense,
        Record.is_deleted == False,
        Record.owner_id == current_user.id

    )
    total_expenses = session.exec(expense_query).scalar() or Decimal("0.00")

    # 3. Calculate Net Balance
    net_balance = total_income - total_expenses


    category_query = select(Record.category, func.sum(Record.amount)).where(
        Record.type == TransactionType.expense,
        Record.is_deleted == False,
        Record.owner_id == current_user.id
    ).group_by(Record.category)
    
    category_results = session.exec(category_query).all()
    
    # Format the results into our Pydantic schema
    category_totals = [
        CategoryTotal(category=row[0], total=row[1] or Decimal("0.00")) 
        for row in category_results
    ]

    recent_query = select(Record).where(
        Record.is_deleted == False,
        Record.owner_id == current_user.id
    ).order_by(desc(Record.date)).limit(5)
    
    recent_activity = session.exec(recent_query).all()

    # Return everything!
    return DashboardSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        category_totals=category_totals,
        recent_activity=recent_activity
    )
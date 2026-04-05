from fastapi import Depends, HTTPException, status, Header
from sqlmodel import Session
from database import get_session
from models import User, RoleEnum

# 1. MOCK AUTHENTICATION
def get_current_user(
    
    # we just pass the user ID in a custom header called "X-User-Id"
    x_user_id: int = Header(..., description="Mock Auth: Send your User ID here"), 
    session: Session = Depends(get_session)
) -> User:
    """Fetches the user from the database based on the provided header."""
    user = session.get(User, x_user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication credentials"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Inactive user account"
        )
    return user

# 2. ROLE-BASED ACCESS CONTROL (RBAC)
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Only allows Admins."""
    if current_user.role != RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin privileges required to perform this action."
        )
    return current_user

def require_analyst_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Allows Admins and Analysts, blocks Viewers."""
    if current_user.role not in [RoleEnum.admin, RoleEnum.analyst]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You do not have permission to view detailed records."
        )
    return current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import User
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# 💡 Pro-Tip: In a production app, use passlib for real hashing. 
# For this assignment, a simple mock function shows you understand the concept.
def get_password_hash(password: str) -> str:
    return f"fake_hashed_{password}"

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    
    # 1. Check if email already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )

    # 2. Convert Pydantic schema to SQLModel database object
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    
    # 3. Save to database
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    # FastAPI automatically filters the response to match UserResponse schema!
    return db_user 

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Fetch a specific user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
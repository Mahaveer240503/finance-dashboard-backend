from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from database import get_session
from models import Record, User, TransactionType
from schemas import RecordCreate, RecordResponse


# Import our new security dependencies!
from dependencies import require_admin, require_analyst_or_admin

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(record: RecordCreate, session: Session = Depends(get_session),current_user: User = Depends(require_admin)): # 👈 Security injected here!
    """Create a new financial record."""
    
    # Unpack the schema data and inject the owner_id manually
    db_record = Record(
        **record.model_dump(), 
        owner_id=current_user.id 
    )
    
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

# 🔒 Admins AND Analysts can view records (Viewers get blocked!)
@router.get("/", response_model=list[RecordResponse])
def get_all_records(
    skip: int = 0,                                    
    limit: int = 100,                                
    category: str | None = None,                     
    type: TransactionType | None = None,             
    session: Session = Depends(get_session),
    current_user: User = Depends(require_analyst_or_admin)
):
    """
    Get all active records with optional pagination and filtering.
    (Analyst/Admin Only)
    """
    query = select(Record).where(Record.is_deleted == False, Record.owner_id == current_user.id 
)

    # Apply Search Filters dynamically if the user provided them
    if category:
        query = query.where(Record.category == category)
    if type:
        query = query.where(Record.type == type)

    # Apply Pagination (Offset and Limit)
    query = query.offset(skip).limit(limit)

    # Execute and return
    records = session.exec(query).all()
    return records

# ONLY Admins can delete records
@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin) # 👈 Security injected here!
):
    """Soft delete a record (Admin Only)."""
    record = session.get(Record, record_id)
    if not record or record.is_deleted:
        raise HTTPException(status_code=404, detail="Record not found")
    
    record.is_deleted = True
    session.add(record)
    session.commit()
    return None
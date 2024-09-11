from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..dependencies import get_db, get_current_user, create_access_token, authenticate_user
from ..config import settings
from datetime import timedelta

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/me", response_model=schemas.User)
def read_user_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/users/{user_id}", response_model=schemas.UserWithReviews)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    reviews = []
    average_rating = None
    if db_user.role == "seller":
        reviews = crud.get_reviews_for_seller(db, user_id)
        average_rating = crud.get_seller_average_rating(db, user_id)
    
    return schemas.UserWithReviews(
        id=db_user.id,
        email=db_user.email,
        role=db_user.role,
        is_active=db_user.is_active,
        reviews_received=reviews,
        average_rating=average_rating
    )

@router.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
    return {"ok": True}

# Rotte per i testi del bot
@router.get("/guide/buying")
def get_buying_guide():
    return {"guide": BUYING_GUIDE}

@router.get("/guide/selling")
def get_selling_guide():
    return {"guide": SELLING_GUIDE}

@router.get("/info/reviews")
def get_review_info():
    return {"info": REVIEW_INFO}

@router.get("/info/support")
def get_support_info():
    return {"info": SUPPORT_INFO}

@router.get("/info/legal")
def get_legal_note():
    return {"note": LEGAL_NOTE}
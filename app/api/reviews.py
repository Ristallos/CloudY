from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/reviews/", response_model=schemas.Review)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    order = crud.get_order(db, review.order_id)
    if not order or order.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorizzato a lasciare una recensione per questo ordine")
    
    existing_review = crud.get_review_by_order(db, review.order_id)
    if existing_review:
        raise HTTPException(status_code=400, detail="Una recensione per questo ordine esiste già")
    
    return crud.create_review(db, review, current_user.id, order.seller_id)

@router.get("/reviews/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Recensione non trovata")
    return db_review

@router.get("/sellers/{seller_id}/reviews/", response_model=List[schemas.Review])
def read_seller_reviews(seller_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_for_seller(db, seller_id, skip=skip, limit=limit)
    return reviews

@router.put("/reviews/{review_id}", response_model=schemas.Review)
def update_review(
    review_id: int,
    review_update: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Recensione non trovata")
    if db_review.reviewer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorizzato a modificare questa recensione")
    return crud.update_review(db, review_id, review_update)

@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_review = crud.get_review(db, review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Recensione non trovata")
    if db_review.reviewer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorizzato a eliminare questa recensione")
    crud.delete_review(db, review_id)

@router.get("/sellers/{seller_id}/average-rating", response_model=float)
def get_seller_average_rating(seller_id: int, db: Session = Depends(get_db)):
    return crud.get_seller_average_rating(db, seller_id)
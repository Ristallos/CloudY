from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas
from typing import List, Optional
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_user_product(db: Session, product: schemas.ProductCreate, user_id: int):
    db_product = models.Product(**product.dict(), seller_id=user_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    db_order = models.Order(customer_id=user_id, status="pending")
    for item in order.items:
        db_order.items.append(models.OrderItem(**item.dict()))
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_review(db: Session, review_id: int) -> Optional[models.Review]:
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_reviews_for_seller(db: Session, seller_id: int, skip: int = 0, limit: int = 100) -> List[models.Review]:
    return db.query(models.Review).filter(models.Review.seller_id == seller_id).offset(skip).limit(limit).all()

def create_review(db: Session, review: schemas.ReviewCreate, customer_id: int, seller_id: int) -> models.Review:
    db_review = models.Review(**review.dict(), reviewer_id=customer_id, seller_id=seller_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, review_update: schemas.ReviewCreate) -> Optional[models.Review]:
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        update_data = review_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int) -> bool:
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False

def get_seller_average_rating(db: Session, seller_id: int) -> float:
    result = db.query(func.avg(models.Review.rating)).filter(models.Review.seller_id == seller_id).scalar()
    return float(result) if result else 0.0

def get_review_by_order(db: Session, order_id: int) -> Optional[models.Review]:
    return db.query(models.Review).filter(models.Review.order_id == order_id).first()

def create_delivery(db: Session, delivery: schemas.DeliveryCreate):
    db_delivery = models.Delivery(**delivery.dict())
    db.add(db_delivery)
    db.commit()
    db.refresh(db_delivery)
    return db_delivery

def get_deliveries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Delivery).offset(skip).limit(limit).all()

def get_delivery(db: Session, delivery_id: int):
    return db.query(models.Delivery).filter(models.Delivery.id == delivery_id).first()

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['hashed_password'] = pwd_context.hash(update_data['password'])
            del update_data['password']
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
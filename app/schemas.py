from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    rating: float
    comment: str
    order_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    seller_id: int
    reviewer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserWithReviews(User):
    reviews_received: List[Review] = []
    average_rating: Optional[float] = None

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    seller_id: int

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: int

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    order_date: datetime
    status: str
    items: List[OrderItem]
    review: Optional[Review] = None

    class Config:
        orm_mode = True

class DeliveryBase(BaseModel):
    order_id: int
    courier_id: int
    status: str

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryBase):
    id: int
    delivery_date: Optional[datetime]

    class Config:
        orm_mode = True
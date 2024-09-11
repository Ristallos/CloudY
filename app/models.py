from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)  # Può essere 'customer', 'seller', o 'courier'
    
    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="customer")
    reviews_received = relationship("Review", foreign_keys="[Review.seller_id]", back_populates="seller")
    reviews_given = relationship("Review", foreign_keys="[Review.reviewer_id]", back_populates="reviewer")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    seller_id = Column(Integer, ForeignKey("users.id"))
    
    seller = relationship("User", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)
    
    customer = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    delivery = relationship("Delivery", back_populates="order", uselist=False)
    review = relationship("Review", back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    rating = Column(Float)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    seller = relationship("User", foreign_keys=[seller_id], back_populates="reviews_received")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
    order = relationship("Order", back_populates="review")


class SellerReview(Base):
    __tablename__ = "seller_reviews"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Float)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    seller = relationship("User", foreign_keys=[seller_id], back_populates="reviews_received")
    reviewer = relationship("User", foreign_keys=[reviewer_id], back_populates="reviews_given")
"""
Database Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    display_name = Column(String(255))
    phone_number = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime)
    passport_number = Column(String(255))  # Will be encrypted per SP-189
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user")

class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    distance_miles = Column(Float)
    travel_duration_hours = Column(Integer)
    base_price_usd = Column(Float, nullable=False)
    min_age_requirement = Column(Integer, default=21)
    max_capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
    
    bookings = relationship("Booking", back_populates="destination")

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    reference_code = Column(String(20), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    departure_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=False)
    num_travelers = Column(Integer, nullable=False)
    final_amount = Column(Float, nullable=False)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="bookings")
    destination = relationship("Destination", back_populates="bookings")

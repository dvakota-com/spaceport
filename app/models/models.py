"""
Database Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()


class BookingStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    REFUNDED = "refunded"  # Added for payment tracking


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))  # Renamed from display_name
    phone_number = Column(String(50))  # Made optional for faster signup
    date_of_birth = Column(DateTime, nullable=False)
    passport_number = Column(String(255))  # Will be encrypted per SP-189
    loyalty_points = Column(Integer, default=0)
    loyalty_tier = Column(String(50), default="bronze")  # Auto-calculated tier
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user")


class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    distance_km = Column(Float)  # Changed to km for international users
    travel_duration_hours = Column(Integer)
    base_price_usd = Column(Float, nullable=False)
    risk_level = Column(Integer)  # 1-5 risk assessment
    min_age_requirement = Column(Integer, default=18)  # Lowered from 21
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
    return_date = Column(DateTime)  # Made optional for one-way trips
    passenger_count = Column(Integer, nullable=False)  # Renamed from num_travelers
    total_price = Column(Float, nullable=False)  # Renamed from final_amount
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="bookings")
    destination = relationship("Destination", back_populates="bookings")


class WaitlistEntry(Base):
    """
    Waitlist for fully booked destinations - SP-156
    """
    __tablename__ = "waitlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    desired_date = Column(DateTime)
    passenger_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

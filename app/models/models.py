"""
Database Models
Schema version: 3.0
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
    REFUNDED = "refunded"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))  # Renamed from display_name for consistency
    phone_number = Column(String(50))  # Made optional per UX feedback
    date_of_birth = Column(DateTime)
    passport_number = Column(String(255))  # Encrypted at rest (SP-189)
    nationality = Column(String(100))
    loyalty_points = Column(Integer, default=0)
    loyalty_tier = Column(String(50), default="bronze")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookings = relationship("Booking", back_populates="user")


class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    distance_km = Column(Float)  # Changed from miles to km (international)
    travel_duration_hours = Column(Integer)
    base_price_usd = Column(Float, nullable=False)
    risk_level = Column(Integer)  # 1-5 scale
    min_age_requirement = Column(Integer, default=18)  # Lowered from 21
    max_capacity = Column(Integer)
    current_availability = Column(Integer)
    is_active = Column(Boolean, default=True)
    launch_site = Column(String(255))
    
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
    discount_applied = Column(Float, default=0)
    discount_code = Column(String(50))
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    special_requests = Column(Text)
    insurance_included = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # TODO: Add seat_class field (SP-203)
    
    user = relationship("User", back_populates="bookings")
    destination = relationship("Destination", back_populates="bookings")


class WaitlistEntry(Base):
    """Waitlist for sold-out destinations"""
    __tablename__ = "waitlist"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    desired_date = Column(DateTime)
    passenger_count = Column(Integer, default=1)
    priority_score = Column(Integer, default=0)
    notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

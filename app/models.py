# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String, unique=True, nullable=False)
    channel = Column(String)
    
    # Define the relationship to rooms
    rooms = relationship("Room", back_populates="customer")

class Room(Base):
    __tablename__ = "room"
    room_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    status = Column(String(20), default="ongoing")
    channel = Column(String(100))
    phone_number = Column(String(20))
    messages = relationship("Message", back_populates="room", cascade="all, delete-orphan")
    funnels = relationship("Funnel", back_populates="room")
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="rooms")

class Message(Base):
    __tablename__ = "message"
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("room.room_id", ondelete="CASCADE"), nullable=False)
    sender_type = Column(String(20), nullable=False)  # customer, agent, system
    contents = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    channel = Column(String(100))
    phone_number = Column(String(20))
    room = relationship("Room", back_populates="messages")

class Funnel(Base):
    __tablename__ = "funnel"
    lead_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("room.room_id", ondelete="SET NULL"))
    lead_date = Column(DateTime, nullable=False)
    channel = Column(String(100))
    phone_number = Column(String(20))
    booking_date = Column(DateTime)
    transaction_date = Column(DateTime)
    transaction_value = Column(Numeric(12, 2))

    room = relationship("Room", back_populates="funnels")

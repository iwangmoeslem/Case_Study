from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class MessageCreate(BaseModel):
    content: str
    sender_type: str  # 'customer', 'agent', 'system'
    timestamp: datetime

class RoomCreate(BaseModel):
    room_id: str
    channel: str
    phone_number: str
    messages: List[MessageCreate]

class IngestMessage(BaseModel):
    phone_number: str
    room_id: UUID
    message: str
    channel: str
    sender: str
    booking_date: datetime
    transaction_date: datetime
    transaction_value: float

class IngestResponse(BaseModel):
    status: str
    room_id: UUID

    class Config:
        orm_mode = True

class Room(BaseModel):
    room_id: UUID
    start_time: datetime
    end_time: datetime | None = None
    status: str = 'ongoing'
    channel: str | None = None
    phone_number: str | None = None

    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    phone_number: str
    channel: Optional[str] = "unknown"

class Customer(BaseModel):
    id: UUID
    phone_number: str
    channel: Optional[str]

    class Config:
        orm_mode = True

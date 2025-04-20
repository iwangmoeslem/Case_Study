from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.database import init_db
from app.schemas import IngestMessage
from uuid import UUID
from datetime import datetime
from typing import List
from app.keywords import get_opening_keywords


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
init_db()

@app.get("/")
def read_root():
    return {"message": "Hello, Sparks Sports Academy 🚀"}



# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/rooms/{room_id}", response_model=schemas.Room)
def get_room_info(room_id: UUID, db: Session = Depends(get_db)):
    # Query the room by room_id
    room = db.query(models.Room).filter(models.Room.room_id == room_id).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    return room

@app.get("/customers", response_model=List[schemas.Customer])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return customers


@app.post("/ingest_message")
async def ingest_message(payload: IngestMessage, db: Session = Depends(get_db)):
    try:
        phone = payload.phone_number
        channel = payload.channel
        room_id = payload.room_id
        message = payload.message
        sender = payload.sender

        keywords = get_opening_keywords()

        # Get or create customer
        customer = db.query(models.Customer).filter_by(phone_number=phone).first()
        if not customer:
            customer = models.Customer(phone_number=phone, channel=channel)
            db.add(customer)
            db.commit()
            db.refresh(customer)

        # Get or create room
        room = db.query(models.Room).filter_by(room_id=room_id).first()
        if not room:
            room = models.Room(
                room_id=room_id,
                customer_id=customer.id,
                start_time=datetime.utcnow(),  
                channel=channel,
                phone_number=phone
            )
            db.add(room)
            db.commit()
            db.refresh(room)

        # Create message
        msg = models.Message(
            room_id=room.room_id,  
            contents=message,      
            sender_type=sender,
            channel=channel,
            phone_number=phone
        )
        db.add(msg)
        db.commit()

        #If it's the opening keyword, create a funnel
        if any(keyword in message for keyword in keywords):
            existing_funnel = db.query(models.Funnel).filter_by(room_id=room.room_id).first()
            if not existing_funnel:
                funnel = models.Funnel(
                    room_id=room.room_id,
                    lead_date=datetime.utcnow(),
                    channel=channel,
                    phone_number=phone,
                    booking_date=payload.booking_date,
                    transaction_date=payload.transaction_date,
                    transaction_value=payload.transaction_value
                    # booking_date, transaction_date, transaction_value can be updated later
                )
                db.add(funnel)
                db.commit()

        return {"status": "success", "room_id": room.room_id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/customers", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Check if customer already exists
    existing_customer = db.query(models.Customer).filter_by(phone_number=customer.phone_number).first()
    if existing_customer:
        raise HTTPException(status_code=400, detail="Customer already exists")

    new_customer = models.Customer(
        phone_number=customer.phone_number,
        channel=customer.channel
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

import logging
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Address Book API",
    description="A RESTful API for managing addresses with coordinate-based distance queries",
    version="1.0.0",
    contact={
        "name": "Address Book API Support",
        "email": "support@addressbook.api",
    },
)

@app.on_event("startup")
async def startup_event():
    logger.info("Address Book API starting up...")
    logger.info("Database tables created/verified")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Address Book API shutting down...")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to the Address Book API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.post("/addresses/", response_model=schemas.Address, tags=["Addresses"])
def create_address(
    address: schemas.AddressCreate,
    db: Session = Depends(get_db)
):
    
    try:
        return crud.create_address(db=db, address=address)
    except Exception as e:
        logger.error(f"Error creating address: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error creating address: {str(e)}")

@app.get("/addresses/", response_model=List[schemas.Address], tags=["Addresses"])
def read_addresses(
    skip: int = Query(0, ge=0, description="Number of addresses to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of addresses to return"),
    db: Session = Depends(get_db)
):
    
    try:
        addresses = crud.get_addresses(db, skip=skip, limit=limit)
        return addresses
    except Exception as e:
        logger.error(f"Error retrieving addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving addresses")

@app.get("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
def read_address(address_id: int, db: Session = Depends(get_db)):
    
    db_address = crud.get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.put("/addresses/{address_id}", response_model=schemas.Address, tags=["Addresses"])
def update_address(
    address_id: int,
    address_update: schemas.AddressUpdate,
    db: Session = Depends(get_db)
):
    
    db_address = crud.update_address(db, address_id=address_id, address_update=address_update)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.delete("/addresses/{address_id}", tags=["Addresses"])
def delete_address(address_id: int, db: Session = Depends(get_db)):
    
    success = crud.delete_address(db, address_id=address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": f"Address {address_id} deleted successfully"}

@app.post("/addresses/nearby/", response_model=List[schemas.Address], tags=["Addresses"])
def get_nearby_addresses(
    query: schemas.AddressDistanceQuery,
    db: Session = Depends(get_db)
):
    
    try:
        addresses = crud.get_addresses_within_distance(
            db, 
            lat=query.latitude, 
            lng=query.longitude, 
            distance_km=query.distance_km
        )
        return addresses
    except Exception as e:
        logger.error(f"Error finding nearby addresses: {str(e)}")
        raise HTTPException(status_code=500, detail="Error finding nearby addresses")

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "message": "Address Book API is running"}

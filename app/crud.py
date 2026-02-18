import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import calculate_distance

logger = logging.getLogger(__name__)

def create_address(db: Session, address: schemas.AddressCreate) -> models.Address:
    
    logger.info(f"Creating new address in {address.city}, {address.country}")
    
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    
    logger.info(f"Address created with ID: {db_address.id}")
    return db_address

def get_address(db: Session, address_id: int) -> Optional[models.Address]:
    logger.info(f"Retrieving address with ID: {address_id}")
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def get_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[models.Address]:
    
    logger.info(f"Retrieving addresses (skip: {skip}, limit: {limit})")
    return db.query(models.Address).offset(skip).limit(limit).all()

def update_address(db: Session, address_id: int, address_update: schemas.AddressUpdate) -> Optional[models.Address]:
    
    logger.info(f"Updating address with ID: {address_id}")
    
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        # Update only provided fields
        update_data = address_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_address, field, value)
        
        db.commit()
        db.refresh(db_address)
        logger.info(f"Address {address_id} updated successfully")
        return db_address
    
    logger.warning(f"Address {address_id} not found for update")
    return None

def delete_address(db: Session, address_id: int) -> bool:
    
    logger.info(f"Deleting address with ID: {address_id}")
    
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        logger.info(f"Address {address_id} deleted successfully")
        return True
    
    logger.warning(f"Address {address_id} not found for deletion")
    return False

def get_addresses_within_distance(
    db: Session, 
    lat: float, 
    lng: float, 
    distance_km: float
) -> List[models.Address]:
    
    logger.info(f"Searching addresses within {distance_km}km of ({lat}, {lng})")
    
    all_addresses = db.query(models.Address).all()
    nearby_addresses = []
    
    for address in all_addresses:
        distance = calculate_distance(lat, lng, address.latitude, address.longitude)
        if distance <= distance_km:
            nearby_addresses.append(address)
    
    logger.info(f"Found {len(nearby_addresses)} addresses within {distance_km}km")
    return nearby_addresses

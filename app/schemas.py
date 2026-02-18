from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

class AddressBase(BaseModel):
    street: str = Field(..., min_length=1, max_length=255, description="Street address")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    state: Optional[str] = Field(None, max_length=100, description="State or province")
    country: str = Field(..., min_length=1, max_length=100, description="Country")
    postal_code: Optional[str] = Field(None, max_length=20, description="Postal or ZIP code")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate (-90 to 90)")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate (-180 to 180)")

    @validator('street', 'city', 'country')
    def validate_non_empty_strings(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or only whitespace')
        return v.strip()

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    street: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class Address(AddressBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class AddressDistanceQuery(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Center point latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Center point longitude")  
    distance_km: float = Field(..., gt=0, description="Maximum distance in kilometers")

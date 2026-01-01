from datetime import date
from pydantic import BaseModel, Field


class RentalCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    start_date: date
    end_date: date


class RentalOut(BaseModel):
    rental_id: int
    car_id: int
    customer_name: str
    start_date: date
    end_date: date
    completed: bool

    model_config = {"from_attributes": True}

from pydantic import BaseModel, Field
from app.models.car import CarStatus


class CarCreate(BaseModel):
    model: str = Field(min_length=1, max_length=120)
    year: int = Field(ge=1886, le=2100)


class CarOut(CarCreate):
    id: int
    status: CarStatus

    model_config = {"from_attributes": True}

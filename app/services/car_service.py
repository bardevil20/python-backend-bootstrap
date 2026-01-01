from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.car import Car
from app.services.errors import NotFoundError


def create_car(db: Session, model: str, year: int) -> Car:
    car = Car(model=model, year=year)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def list_cars(db: Session) -> list[Car]:
    return list(db.scalars(select(Car).order_by(Car.id.asc())))


def get_car(db: Session, car_id: int) -> Car:
    car = db.get(Car, car_id)
    if not car:
        raise NotFoundError(f"Car with id {car_id} not found")
    return car

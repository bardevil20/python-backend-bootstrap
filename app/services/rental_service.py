from sqlalchemy.orm import Session

from app.models.car import CarStatus
from app.models.rental import Rental
from app.services.errors import NotFoundError, BadRequestError


def create_rental_for_car(
    db: Session,
    car,
    customer_name: str,
    start_date,
    end_date,
) -> Rental:
    if end_date < start_date:
        raise BadRequestError("end_date must be >= start_date")

    if car.status != CarStatus.AVAILABLE:
        raise BadRequestError("car is not available")

    rental = Rental(
        car_id=car.id,
        customer_name=customer_name,
        start_date=start_date,
        end_date=end_date,
        completed=False,
    )
    car.status = CarStatus.RENTED

    db.add_all([rental, car])
    db.commit()
    db.refresh(rental)
    return rental


def complete_rental(db: Session, rental_id: int) -> Rental:
    rental = db.get(Rental, rental_id)
    if not rental:
        raise NotFoundError(f"Rental with id {rental_id} not found")

    if rental.completed:
        return rental

    car = db.get(type(rental).car.property.mapper.class_, rental.car_id)
    if not car:
        raise BadRequestError("car not found for this rental")

    rental.completed = True
    car.status = CarStatus.AVAILABLE

    db.add_all([rental, car])
    db.commit()
    db.refresh(rental)
    return rental

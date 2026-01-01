from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.car import CarCreate, CarOut
from app.schemas.rental import RentalCreate, RentalOut
from app.services.car_service import create_car, list_cars, get_car
from app.services.rental_service import create_rental_for_car
from app.services.errors import NotFoundError, BadRequestError

router = APIRouter(prefix="/api/cars", tags=["cars"])


@router.post("", response_model=CarOut, status_code=status.HTTP_201_CREATED)
def create_car_route(payload: CarCreate, db: Session = Depends(get_db)):
    return create_car(db, model=payload.model, year=payload.year)


@router.get("", response_model=list[CarOut])
def list_cars_route(db: Session = Depends(get_db)):
    return list_cars(db)


@router.post("/{car_id}/rentals", response_model=RentalOut, status_code=status.HTTP_201_CREATED)
def create_rental_for_car_route(car_id: int, payload: RentalCreate, db: Session = Depends(get_db)):
    try:
        car = get_car(db, car_id)
        return create_rental_for_car(
            db,
            car=car,
            customer_name=payload.customer_name,
            start_date=payload.start_date,
            end_date=payload.end_date,
        )
    except NotFoundError as e:
        raise HTTPException(404, str(e))
    except BadRequestError as e:
        raise HTTPException(400, str(e))

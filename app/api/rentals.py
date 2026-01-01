from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.rental import RentalOut
from app.services.rental_service import complete_rental
from app.services.errors import NotFoundError, BadRequestError

router = APIRouter(prefix="/api/rentals", tags=["rentals"])


@router.post("/{rental_id}/complete", response_model=RentalOut)
def complete_rental_route(rental_id: int, db: Session = Depends(get_db)):
    try:
        return complete_rental(db, rental_id)
    except NotFoundError as e:
        raise HTTPException(404, str(e))
    except BadRequestError as e:
        raise HTTPException(400, str(e))

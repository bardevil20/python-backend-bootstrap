import enum
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class CarStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RENTED = "RENTED"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[CarStatus] = mapped_column(
        Enum(CarStatus, name="car_status_enum"),
        nullable=False,
        default=CarStatus.AVAILABLE,
        server_default=CarStatus.AVAILABLE.value,
    )
    rentals: Mapped[list["Rental"]] = relationship(back_populates="car")

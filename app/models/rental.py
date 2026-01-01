from sqlalchemy import String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Rental(Base):
    __tablename__ = "rentals"

    rental_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), nullable=False)

    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    start_date: Mapped[object] = mapped_column(Date, nullable=False)
    end_date: Mapped[object] = mapped_column(Date, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    car: Mapped["Car"] = relationship(back_populates="rentals")

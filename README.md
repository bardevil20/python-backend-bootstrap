# python-backend-bootstrap

## What this repo for?

A step-by-step Python backend bootstrap repository.
This repo is is a hands-on step-by-step Python adaptation, inspired by the “Modern Backend Meetup” repo https://github.com/nivitzhaky/modern-backend-meetup by @nivitzhaky.

The goal of this repository is to guide you from **an empty repo** to a **working, production-style backend** by building everything incrementally:
- FastAPI service that answers APIs
- PostgreSQL with Docker
- SQLAlchemy + Alembic migrations
- CRUD example
- Dockerized API
- Deployment to EC2

---

## Stack

- **Python 3.14.1**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy 2**
- **Alembic**
- **Docker / docker-compose**
- Dependency management via **requirements.txt**

---

## Follow the steps below to run the project

## GIT — fork & clone

**macOS / Linux** OR **Windows (PowerShell)**

```
git clone https://github.com/<YOUR_USER>/python-backend-bootstrap.git
cd python-backend-bootstrap
```

---

## STEP 1 — Create a fresh FastAPI skeleton (from scratch)

### 1.1 Prerequisites

* Python **3.14.1**
* pip

**macOS / Linux**

```bash
python3 --version
pip3 --version
```

**Windows (PowerShell)**

```powershell
python --version
pip --version
```

---

### 1.2 Create folders & files

**macOS / Linux**

```bash
mkdir -p app/api app/core app/db app/models app/schemas tests
touch app/__init__.py app/main.py
touch app/api/__init__.py app/api/cars.py app/api/rentals.py
touch app/core/__init__.py app/core/config.py
touch requirements.txt .env.example .gitignore
```

**Windows (PowerShell)**

```powershell
mkdir app, tests
mkdir app\api, app\core, app\db, app\models, app\schemas

New-Item app\__init__.py -ItemType File
New-Item app\main.py -ItemType File
New-Item app\api\__init__.py -ItemType File
New-Item app\api\cars.py -ItemType File
New-Item app\api\rentals.py -ItemType File
New-Item app\core\__init__.py -ItemType File
New-Item app\core\config.py -ItemType File
New-Item requirements.txt -ItemType File
New-Item .env.example -ItemType File
New-Item .gitignore -ItemType File
```

---

### 1.3 Dependencies

`requirements.txt`

```txt
fastapi
uvicorn[standard]

SQLAlchemy
psycopg[binary]

alembic

pydantic
pydantic-settings

pytest
httpx
```

---

### 1.4 Virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r requirements.txt
```

---

### 1.5 Environment variables

`.env.example`

```env
APP_ENV=local
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/postgres
```

Create `.env`

**macOS / Linux**

```bash
cp .env.example .env
```

**Windows (PowerShell)**

```powershell
Copy-Item .env.example .env
```

---

### 1.6 Config loader

`app/core/config.py`

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
```

---

### 1.7 Minimal API (health + routers)

`app/main.py`

```python
from fastapi import FastAPI

app = FastAPI(title="python-backend-bootstrap")

@app.get("/health")
def health():
    return {"status": "ok"}

```

---

### 1.8 Run the service

**macOS / Linux** OR **Windows (PowerShell)**

```bash
uvicorn app.main:app --reload
```

Check health:

* [http://localhost:8000/health](http://localhost:8000/health)

---

### 1.9 Initial commit

```bash
git add .
git commit -m "step 1 - fastapi skeleton"
```

---

## STEP 2 — PostgreSQL with Docker

`docker-compose.yml`

```yaml
version: "3.9"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgresdata:/var/lib/postgresql/data

volumes:
  postgresdata:
```

Update config file

`app/core/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
```

**macOS / Linux** OR **Windows (PowerShell)**

```bash
docker compose up -d db
```

Commit:

```bash
git add docker-compose.yml
git commit -m "step 2 - postgres with docker"
```

---

## STEP 3 — Database session (SQLAlchemy)

Create files:

**macOS / Linux**

```bash
touch app/db/__init__.py app/db/base.py app/db/session.py
```

**Windows (PowerShell)**

```powershell
New-Item app\db\__init__.py -ItemType File
New-Item app\db\base.py -ItemType File
New-Item app\db\session.py -ItemType File
```

`app/db/base.py`

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

`app/db/session.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def _require_db_url() -> str:
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return settings.database_url


engine = create_engine(_require_db_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Commit:

```bash
git add app/db
git commit -m "step 3 - sqlalchemy session"
```

---

## STEP 4 — Alembic migrations

### 4.1 Initialize Alembic

**macOS / Linux** Or **Windows (PowerShell)**

```bash
alembic init alembic
```

### 4.2 Update `alembic/env.py`

Add the following near the top of `alembic/env.py` (after Alembic imports):

```python
from app.core.config import settings
from app.db.base import Base
import app.models

config.set_main_option("sqlalchemy.url", settings.database_url or "")
target_metadata = Base.metadata
```

Create `app/models/__init__.py` if missing:

**macOS / Linux**

```bash
touch app/models/__init__.py
```

**Windows (PowerShell)**

```powershell
New-Item app\models\__init__.py -ItemType File
```

You will populate it in STEP 5.

Commit:

```bash
git add alembic alembic.ini
git commit -m "step 4 - alembic setup"
```

---

## STEP 5 — Minimal CRUD (Cars + Rentals) — write the files

This step adds two related tables:

* `cars`: `id`, `model`, `year`, `status`, `created_at`
* `rentals`: `rental_id`, `car_id (FK)`, `customer_name`, `start_date`, `end_date`, `completed`

Endpoints included:

* `POST /api/cars` (create car)
* `GET /api/cars` (list cars)
* `POST /api/cars/{car_id}/rentals` (create rental for a car + sets car status to RENTED)
* `POST /api/rentals/{rental_id}/complete` (complete rental + sets car status to AVAILABLE)

---

### 5.1 Models (SQLAlchemy)

Create: `app/models/car.py`

```python
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

```

Create: `app/models/rental.py`

```python
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

```

Update: `app/models/__init__.py`

```python
from .car import Car, CarStatus
from .rental import Rental
```

---

### 5.2 Schemas (Pydantic)

Create: `app/schemas/car.py`

```python
from pydantic import BaseModel, Field
from app.models.car import CarStatus


class CarCreate(BaseModel):
    model: str = Field(min_length=1, max_length=120)
    year: int = Field(ge=1886, le=2100)


class CarOut(CarCreate):
    id: int
    status: CarStatus

    model_config = {"from_attributes": True}
```

Create: `app/schemas/rental.py`

```python
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
```

---


### 5.3 Services errors (domain-level exceptions)

Create shared exceptions for the service layer.  
The API layer will translate them to HTTP responses.

Create: `app/services/errors.py`

```python
class NotFoundError(Exception):
    pass


class BadRequestError(Exception):
    pass

```
---

### 5.4 Services (DB operations)
`app/services/car_service.py`

```python
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

```

`app/services/rental_service.py`

```python
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

```
---

### 5.5 Routes (FastAPI) — thin controllers
`app/api/cars.py`

```python
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

```

`app/api/rentals.py`

```python
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

```

---

### 5.6 Create migration & upgrade DB

**macOS / Linux** OR **Windows (PowerShell)**

```bash
alembic revision --autogenerate -m "create cars and rentals"
```

This command would generate a new migration file, under alembic/versions dir, named <revision_id>_create_cars_and_rentals.
Update file content with tables creation migrations:

`alembic/versions/<revision_id_create_cars_and_rentals`

```python
"""create cars and rentals

Revision ID: 5b9e02912791
Revises: 
Create Date: 2025-12-29 15:55:24.192742

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b9e02912791'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=120), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'RENTED', name='cars_status_enum'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rentals',
    sa.Column('rental_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(length=120), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.PrimaryKeyConstraint('rental_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

```

Run migrations:
```bash
alembic upgrade head
```

Update app/main.py:

`app/main.py`
```python
from fastapi import FastAPI
from app.api.cars import router as cars_router
from app.api.rentals import router as rentals_router

app = FastAPI(title="python-backend-bootstrap")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(cars_router)
app.include_router(rentals_router)

```

---

### 5.7 Quick API examples (minimal)

Assuming the server is running on `http://localhost:8000`

#### Create a car

**macOS / Linux**

```bash
curl -s -X POST http://localhost:8000/api/cars \
  -H "Content-Type: application/json" \
  -d '{"model":"Mazda 3","year":2020}'
```

**Windows (PowerShell)**

```powershell
$body = @{ model="Mazda 3"; year=2020 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/cars" -ContentType "application/json" -Body $body
```

#### Create a rental for that car

**macOS / Linux**

```bash
curl -s -X POST http://localhost:8000/api/cars/1/rentals \
  -H "Content-Type: application/json" \
  -d '{"customer_name":"Niv","start_date":"2025-01-01","end_date":"2025-01-05"}'
```

**Windows (PowerShell)**

```powershell
$body = @{ customer_name="Niv"; start_date="2025-01-01"; end_date="2025-01-05" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/cars/1/rentals" -ContentType "application/json" -Body $body
```

#### Complete the rental

**macOS / Linux**

```bash
curl -s -X POST http://localhost:8000/api/rentals/1/complete
```

**Windows (PowerShell)**

```powershell
Invoke-RestMethod -Method Post "http://localhost:8000/api/rentals/1/complete"
```

Commit:

```bash
git add app/models app/schemas app/services app/api app/main.py
git commit -m "step 5 - cars and rentals minimal crud with service layer"
```

---

## STEP 6 — Dockerize the API

### Create docker file
* What is a Dockerfile?
  A **Dockerfile** is the “recipe” for building **one image** (usually one service).
  In this repo it builds the **API image**:
  - takes a base image (python)
  - installs `requirements.txt`
  - copies your code
  - defines how to start the server (`uvicorn ...`)
  You use it when you want: `docker build ...` (or when docker-compose builds for you).
---

`Dockerfile`

```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Update `docker-compose.yml` to include both services:

* What is docker-compose.yml?
  `docker-compose.yml` describes **how to run multiple containers together** (a small stack):
  - which services to run (api, db, etc.)
  - networking between them
  - ports, environment variables, volumes
  - startup order (`depends_on`)
  
  You use it when you want one command to bring up the whole stack:
  `docker compose up ...`

---

`docker-compose.yml`

```yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./postgresdata:/var/lib/postgresql/data
  app:
      build: .
      environment:
        - APP_ENV=local
        - DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/postgres
      ports:
        - "8000:8000"
      depends_on:
        - db
  alembic:
    build: .
    environment:
      - APP_ENV=local
      - DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/postgres
    depends_on:
      - db
    command: ["alembic", "upgrade", "head"]
    
volumes:
  postgresdata:
```

Key points:
* build: . tells Compose to build the API image using the Dockerfile in this repo.
* In DATABASE_URL, the host is db (the service name), not localhost.
* depends_on ensures db starts before api (it does not guarantee DB is “ready”, only started).

### ### Run API + PostgreSQL together via docker

first make sure db is not running over docker from previous steps,
use command `docker compose down -v` to shut all docker containers.

**macOS / Linux** OR **Windows (PowerShell)**

```bash
docker compose down -v
docker compose up -d --build
```

---

## STEP 8 — Deploy to EC2

### 8.1 Create EC2 instance

* Ubuntu Server 22.04
* Instance type: `t3.micro`
* Open ports: 22, 80, 8000
* Download key pair (`.pem`)

---

### 8.2 Connect via SSH

**macOS / Linux**

```bash
chmod 400 my-key.pem
ssh -i my-key.pem ubuntu@X.X.X.X
```

**Windows (PowerShell)**

```powershell
ssh -i my-key.pem ubuntu@X.X.X.X
```

---

### 8.3 Install Docker on EC2

```bash
sudo apt update
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
exit
```

Reconnect and verify:

```bash
docker --version
docker compose version
```

---

### 8.4 Run the project on EC2

```bash
git clone https://github.com/<YOUR_USER>/python-backend-bootstrap.git
cd python-backend-bootstrap
cp .env.example .env
docker compose up -d --build
```

---

### 8.5 Verify deployment

* [http://X.X.X.X:8000/health](http://X.X.X.X:8000/health)
* [http://X.X.X.X:8000/docs](http://X.X.X.X:8000/docs)

---

## How to use this repository as a template

### Option 1 — GitHub template

1. Click **Use this template**
2. Create new repository
3. Clone and start coding

### Option 2 — Manual bootstrap

**macOS / Linux**

```bash
git clone https://github.com/<YOUR_USER>/python-backend-bootstrap.git my-project
cd my-project
rm -rf .git
git init
git commit --allow-empty -m "initial commit"
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/<YOUR_USER>/python-backend-bootstrap.git my-project
cd my-project
Remove-Item -Recurse -Force .git
git init
git commit --allow-empty -m "initial commit"
```

---

### License

MIT License

Copyright (c) 2025 Bar Janah

### Credits

Inspired by the “modern-backend-meetup” repo & meetup recording. 
GitHub @nivitzhaky

---

Happy hacking 🚀

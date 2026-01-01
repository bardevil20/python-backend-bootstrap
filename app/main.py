from fastapi import FastAPI
from app.api.cars import router as cars_router
from app.api.rentals import router as rentals_router

app = FastAPI(title="python-backend-bootstrap")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(cars_router)
app.include_router(rentals_router)

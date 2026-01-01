from fastapi import FastAPI

app = FastAPI(title="python-backend-bootstrap")

@app.get("/health")
def health():
    return {"status": "ok"}

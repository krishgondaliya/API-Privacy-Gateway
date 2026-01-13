from fastapi import FastAPI
from gateway.app.api.routes import router

app = FastAPI(title="API Privacy Gateway", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(router)

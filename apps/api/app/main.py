from fastapi import FastAPI
from .routes import slack_router

app = FastAPI()

app.include_router(slack_router.router, prefix="/slack")

@app.get("/health")
def health():
    return {"ok": True}

from fastapi import FastAPI
from .routes import slack_ingest

app = FastAPI()

app.include_router(slack_ingest.router, prefix="/slack")

@app.get("/health")
def health():
    return {"ok": True}

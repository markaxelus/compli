from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import json

router = APIRouter()

@router.post("/events")
async def slack_events(request: Request):
    raw = await request.body()
    print("RAW BODY BYTES:", raw)

    try:
        body = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print("JSON parse error:", e)
        return JSONResponse(status_code=400, content={"error": "bad json"})

    if body.get("type") == "url_verification" and "challenge" in body:
        return JSONResponse(content={"challenge": body["challenge"]})

    return JSONResponse(content={"ok": True})

from fastapi import APIRouter, Request, Header, BackgroundTasks
from fastapi.responses import JSONResponse
import json
from ..util.slack_signature import verify_slack_signatures
from ..core.settings import SLACK_SIGNING_SECRET

router = APIRouter()

@router.post("/events")
async def slack_events(
    request: Request,
    background: BackgroundTasks,
    x_slack_signature: str | None = Header(default=None, alias="X-Slack-Signature"), 
    x_slack_request_timestamp: str | None = Header(default=None, alias="X-Slack-Request-Timestamp"), 
    ):
    raw_body = await request.body()

    verify_slack_signatures(SLACK_SIGNING_SECRET, x_slack_signature, x_slack_request_timestamp, raw_body)

    try:
        body = json.loads(raw_body.decode("utf-8"))
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": "bad json"})

    # Must be echoed back to Slack
    if body.get("type") == "url_verification" and "challenge" in body:
        return JSONResponse(content={"challenge": body["challenge"]})
    
    return JSONResponse({"ok": True})

from fastapi import HTTPException
import hmac, hashlib, time
import logging
from ..core.settings import DEFAULT_TOLERANCE_SECONDS

SLACK_VERSION = 'v0'


logger = logging.getLogger(__name__)

""" 
Reference: https://api.slack.com/authentication/verifying-requests-from-slack

Performs two security checks:
1. HMAC-SHA256 signature verification with signing secret
2. Timestamp freshness check to prevent replay atttacks
"""

def verify_slack_signatures(signing_secret: str, 
                            x_slack_signature: str, 
                            x_slack_request_timestamp: str, 
                            raw_body: bytes, 
                            tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS) -> None:
  if not signing_secret:
    raise RuntimeError("SLACK_SIGNING_SECRET not found")
  if not x_slack_signature or not x_slack_request_timestamp:
    raise HTTPException(
      status_code=401, 
      detail="Missing Slack signature headers"
    )
  
  try:
    ts_int = int(x_slack_request_timestamp)
  except (ValueError, TypeError):
    logger.warning(f"Invalid timestamp format: {x_slack_request_timestamp}")
    raise HTTPException(
      status_code=401,
      detail="Invalid Slack timestamp"
    )
  if abs(time.time() - ts_int) > tolerance_seconds:
    raise HTTPException(
      status_code=401,
      detail="Stale Slack request"
    )
  
  base = f"{SLACK_VERSION}:{x_slack_request_timestamp}:{raw_body.decode('utf-8')}".encode('utf-8')
  digest = hmac.new(signing_secret.encode('utf-8'), base, hashlib.sha256).hexdigest()
  expected = f"{SLACK_VERSION}={digest}"
  if not hmac.compare_digest(expected, x_slack_signature):
    raise HTTPException(
      status_code=401,
      detail="Invalid Slack signature"
    )


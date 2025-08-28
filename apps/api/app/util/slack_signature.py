from fastapi import HTTPException
import hmac, hashlib, time
import logging

SLACK_VERSION = 'v0'
DEFAULT_TOLERANCE_SECONDS = 300 # 5m as recommended by slack


logger = logging.getLogger(__name__)

""" 
Reference: https://api.slack.com/authentication/verifying-requests-from-slack

Performs two security checks:
1. HMAC-SHA256 signature verification with signing secret
2. Timestamp freshness check to prevent replay atttacks
"""

def verify_slack_signatures(signing_secret: str, 
                            slack_signature: str | None, 
                            slack_timestamp: str | None, 
                            raw_body: bytes, 
                            tolerance_seconds: int = DEFAULT_TOLERANCE_SECONDS) -> None:
  if not signing_secret:
    raise RuntimeError("SLACK_SIGNING_SECRET not found")
  if not slack_signature or not slack_timestamp:
    raise HTTPException(
      status_code=401, 
      detail="Missing Slack signature headers"
    )
  
  try:
    ts_int = int(slack_timestamp)
  except (ValueError, TypeError):
    logger.warning(f"Invalid timestamp format: {slack_timestamp}")
    raise HTTPException(
      status_code=401,
      detail="Invalid Slack timestamp"
    )
  if abs(time.time() - ts_int) > DEFAULT_TOLERANCE_SECONDS:
    raise HTTPException(
      status_code=401,
      detail="Stale Slack request"
    )
  
  base = f"{SLACK_VERSION}:{slack_timestamp}:{raw_body.decode('utf-8')}".encode('utf-8')
  digest = hmac.new(signing_secret.encode('utf-8'), base, hashlib.sha256).hexdigest()
  expected = f"{SLACK_VERSION}={digest}"
  if not hmac.compare_digest(expected, slack_signature):
    raise HTTPException(
      status_code=401,
      detail="Invalid Slack signature"
    )

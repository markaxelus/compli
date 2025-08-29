import pytest
import time
import hmac
import hashlib
from unittest.mock import patch
from fastapi import HTTPException
from api.app.util.slack_signature import verify_slack_signatures, SLACK_VERSION, DEFAULT_TOLERANCE_SECONDS

class TestSlackSignature:

  def setup(self):
    self.signing_secret = "test_signing_secret_123"
    self.raw_body = b'{}'
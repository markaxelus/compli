import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_TOLERANCE_SECONDS = 300 # 5m as recommended by slack
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
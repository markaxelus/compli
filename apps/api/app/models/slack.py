from pydantic import BaseModel

class SlackEnvelope(BaseModel):
  type: str
  challenge: str | None = None
  team_id: str | None = None
  event: dict | None = None
  event_id: str | None = None
  event_time: str | None = None
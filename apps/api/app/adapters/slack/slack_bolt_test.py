from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.event("message")
def handle_message_events(body, say):
    print("RAW BODY:", body)   
    say("Hello, I got your message!")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()

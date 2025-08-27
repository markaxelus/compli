from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("SLACK_BOT")
app_token = os.getenv("SLACK_APP")
print(f"Bot token loaded: {'Yes' if bot_token else 'No'}")
print(f"App token loaded: {'Yes' if app_token else 'No'}")

app = App(token=bot_token)

@app.event("app_mention")
def handle_app_mention(body, say):
    print("App mention received!")
    try:
        say("Compli responded")
        print("✅ Response sent successfully!")
    except Exception as e:
        print(f"❌ Error sending response: {e}")


if __name__ == "__main__":
    print("Starting Slack bot...")
    handler = SocketModeHandler(app, app_token)
    handler.start()


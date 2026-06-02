import os
import json
import slack_bolt
import slack_sdk
import termcolor

from slack_bolt import App
from slack_sdk.webhook import WebhookClient
from slack_bolt.adapter.socket_mode import SocketModeHandler

import user_join
# This sample slack application uses SocketMode
# For the companion getting started setup guide,
# see: https://docs.slack.dev/tools/bolt-python/getting-started
app = App(token=os.environ.get("SLACK_BOT_TOKEN"), signing_secret=os.environ.get("SLACK_SIGN_SECRET"))


@app.event("team_join") 
def event_team_join(event, say): 
    """
    event_team_join handles what happens when a new member joins the workspace. 
    
    It will a function that sends a welcome message through a direct message to the volunteer,
    then write a message to a channel,

    Args:
        event (_type_): _description_
        say (_type_): _description_
    """
    user_id = event["user"]["id"]
    welcome_json = user_join.user_join_blocks(user_id)
    say(blocks=welcome_json, text="!", channel=user_id)
    user_join.write_to_sheet(event)

if __name__ == "__main__":
    # app.start(int(os.environ.get("PORT", '6050')))
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

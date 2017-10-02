from flask import Flask, request, make_response, Response
import os
import json

from slackclient import SlackClient

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

# Dictionary to store coffee orders. In the real world, you'd want an actual key-value store
COFFEE_ORDERS = {}

# Send a message to the user asking if they would like coffee
user_id = "U0CAV5XME"

order_dm = slack_client.api_call(
  "chat.postMessage",
  as_user=True,
  channel=user_id,
  text="I am Coffeebot ::robot_face::, and I\'m here to help bring you fresh coffee :coffee:",
  attachments=[{
    "text": "",
    "callback_id": user_id + "coffee_order_form",
    "color": "#3AA3E3",
    "attachment_type": "default",
    "actions": [{
      "name": "coffee_order",
      "text": ":coffee: Order Coffee",
      "type": "button",
      "value": "coffee_order"
    }]
  }]
)

# Create a new order for this user in the COFFEE_ORDERS dictionary
COFFEE_ORDERS[user_id] = {
    "order_channel": order_dm["channel"],
    "message_ts": "",
    "order": {}
}


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    message_action = json.loads(request.form["payload"])
    user_id = message_action["user"]["id"]

    if message_action["type"] == "interactive_message":
        # Add the message_ts to the user's order info
        COFFEE_ORDERS[user_id]["message_ts"] = message_action["message_ts"]

        # Show the ordering dialog to the user
        open_dialog = slack_client.api_call(
            "dialog.open",
            trigger_id=message_action["trigger_id"],
            dialog={
                "title": "Request a coffee",
                "submit_label": "Submit Order",
                "callback_id": user_id + "coffee_order_form",
                "elements": [
                    {
                        "label": "Coffee Type",
                        "type": "select",
                        "name": "meal_preferences",
                        "placeholder": "Select a drink",
                        "options": [
                            {
                                "label": "Cappuccino",
                                "value": "cappuccino"
                            },
                            {
                                "label": "Latte",
                                "value": "latte"
                            },
                            {
                                "label": "Pour Over",
                                "value": "pour_over"
                            },
                            {
                                "label": "Cold Brew",
                                "value": "cold_brew"
                            }
                        ]
                    }
                ]
            }
        )

        print(open_dialog)

        # Update the message to show that we're in the process of taking their order
        slack_client.api_call(
            "chat.update",
            channel=COFFEE_ORDERS[user_id]["order_channel"],
            ts=message_action["message_ts"],
            text=":pencil: Taking your order...",
            attachments=[]
        )

    elif message_action["type"] == "dialog_submission":
        coffee_order = COFFEE_ORDERS[user_id]

        # Update the message to show that we're in the process of taking their order
        slack_client.api_call(
            "chat.update",
            channel=COFFEE_ORDERS[user_id]["order_channel"],
            ts=coffee_order["message_ts"],
            text=":white_check_mark: Order received!",
            attachments=[]
        )

    return make_response("", 200)


if __name__ == "__main__":
    app.run()

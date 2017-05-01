import os
import sys
import json

import requests
from flask import Flask, request


app = Flask(__name__)

ACCESS_TOKEN = "<YOUR ACCESS TOKEN>"
VERIFY_TOKEN = "<YOUR VERIFY TOKEN>"


@app.route('/', methods=['GET'])
def verify():
	# Used to verify the bot by Facebook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "The Bot Is Working", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint to process incoming messages
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

            	# If it is a message 
                if messaging_event.get("message"): 

                	# Facebook ID of sender
                    sender_id = messaging_event["sender"]["id"]
                    # Page ID        
                    recipient_id = messaging_event["recipient"]["id"]  
                    #Actual Message
                    message_text = messaging_event["message"]["text"]  

                    send_message(sender_id, message_text)

                if messaging_event.get("delivery") or messaging_event.get("optin") or messaging_event.get("postback"):
                	# if any other type of event, just pass
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):
    params = {
        "access_token": ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    response = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if response.status_code != 200:
        print(response.status_code)
        print(response.text)


if __name__ == '__main__':
    app.run()

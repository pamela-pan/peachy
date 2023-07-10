import slack
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, Response
# from slackeventsapi import SlackEventAdapter
import google.generativeai as palm
import string
import random
from slackeventsapi import SlackEventAdapter
from slack_sdk.signature import SignatureVerifier
from slack_sdk.errors import SlackApiError

from flask import Flask, request, Response
from my_modules.welcome import WelcomeMessage
from my_modules.home import HomeDisplay
from my_modules.toneBlocks import TONE_BUTTON_BLOCK
from my_modules.handlers import Handlers
import palm_chat

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
verifier = SignatureVerifier(os.environ['SIGNING_SECRET'])

app = App(token=os.environ["SLACK_BOT_TOKEN"])
handlers = Handlers()

BOT_ID = client.api_call('auth.test')['user_id']
print("bot id", BOT_ID)

welcome_message_list = {}

# boolean statement for bot_status
class Start:
    def __init__(self):
        self.online = False
    def get_status(self):
        return self.online
    def change_status(self):
        self.online = True
        return self.online
    def __str__(self):
        return str(self.online) + str(f' {type(self.online)}')
begin = Start()

class Temperature():
    def __init__(self):
        self.temperature = 0.7
    def set_temperature(self, t):
        self.temperature = t
        return t
thermos = Temperature()

def send_welcome_message(channel, user):
    print("send welcome message working")
    welcome = WelcomeMessage(channel, user)
    message = welcome.get_message()
    response = client.chat_postMessage(text="Welcome Message", **message)
    welcome.timestamp = response['ts']
    
    if channel not in welcome_message_list:
        welcome_message_list[channel] = {}
    welcome_message_list[channel][user] = welcome

@app.event("message")
def message(payload):
    user_id = payload.get('user')
    channel_id = payload.get('channel')
    text = payload.get('text')

    if user_id != None and BOT_ID != user_id:
        if begin == True:
            chat = palm_chat.palmChat(thermos, begin, text)
            client.chat_postMessage(channel=channel_id, text=chat.get_palm_response())
            client.chat_postMessage(channel=channel_id, text="```" + str(chat.catalog) + "```")

@app.action("creative_tone")
def creative_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_creative_tone(ack, body, logger)
    global thermos
    thermos = thermos.set_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {thermos}!\nPlease ask away: ")

@app.action("balanced_tone")
def balanced_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_balanced_tone(ack, body, logger)
    global thermos
    thermos = thermos.set_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {thermos}!\nPlease ask away: ")

@app.action("precise_tone")
def precise_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_precise_tone(ack, body, logger)
    global thermos
    thermos = thermos.set_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {thermos}!\nPlease ask away: ")

@app.event("reaction_added")
def reaction(payload):
    user_id = payload.get('user')
    channel_id = payload.get('item',{}).get('channel')

    if f'@{user_id}' not in welcome_message_list:
        return
    
    welcome = welcome_message_list[f'@{user_id}'][user_id]
    welcome.completed = True
    welcome.channel = channel_id # change channel for welcome message to the actual channel
    message = welcome.get_message()
    updated_message = client.chat_update(**message)
    welcome.timestamp = updated_message['ts']

# home page display
@app.event("app_home_opened")
def open_home(client,event,logger):
    home_display = HomeDisplay(client,event,logger)
    home_display.display_home()

# -- 

@app.command('/start')
def handle_start(ack, body, logger):
    ack()
    logger.info(body)
    channel_id = body['channel_id']
    tone_button_block = TONE_BUTTON_BLOCK
    client.chat_postMessage(channel=channel_id, blocks=tone_button_block["blocks"])
    global begin
    begin = begin.change_status()
    print('/start ', begin)

# --

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

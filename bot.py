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
import documents
import time


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
        self.online = not self.online
        return self
    def __str__(self):
        return str(self.online) + str(f' {type(self.online)}')
switch = Start()

class Temperature():
    def __init__(self):
        self.temperature = 0.7
    def change_temperature(self, t):
        self.temperature = t
        return self
    def get_temperature(self):
        return self.temperature
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
    ts = payload.get('ts')
    print('ts ', ts)

    if user_id is not None and BOT_ID != user_id:
        if switch.get_status() is True:
            # React to the user's message with an emoji
            client.reactions_add(name="speech_balloon", channel=channel_id, timestamp=ts)
                                    
            temp = thermos.get_temperature()
            chat = palm_chat.palmChat(temp, switch, text)

            client.chat_postMessage(channel=channel_id, text=chat.palm_response)


            if documents.DocumentsHandler.current_document_id is None:
                print("New document created")
                documents.DocumentsHandler.create_document(chat.get_current_conversation())
            else:
                print('Document exists, updating')
                documents.DocumentsHandler.update_document(documents.DocumentsHandler.current_document_id, chat.get_current_conversation())

            doc_id = documents.DocumentsHandler.get_document_id()
            print('Current document ID:', doc_id)

            # Pause for a short period to display the reaction
            time.sleep(1)
            
@app.action("creative_tone")
def creative_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_creative_tone(ack, body, logger)
    global thermos
    thermos = thermos.change_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {thermos.get_temperature()}!\nPlease ask away: ")

@app.action("balanced_tone")
def balanced_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_balanced_tone(ack, body, logger)
    global thermos
    thermos = thermos.change_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {thermos.get_temperature()}!\nPlease ask away: ")

@app.action("precise_tone")
def precise_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_precise_tone(ack, body, logger)
    global thermos
    thermos = thermos.change_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {thermos.get_temperature()}!\nPlease ask away: ")

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
    global switch
    switch = switch.change_status()
    print(f'/start status, {switch.get_status()}')

@app.command('/quit')
def handle_start(ack, body, logger):
    ack()
    logger.info(body)
    channel_id = body['channel_id']
    client.chat_postMessage(channel=channel_id, text="You have quit the conversation")
    global switch
    switch = switch.change_status()
    print(f'/quit status, {switch.get_status()}\nTemperature, {thermos.get_temperature()}')

# --

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()



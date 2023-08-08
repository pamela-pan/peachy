import slack
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, Response
from bson import ObjectId
from documents import DocumentsHandler
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
from palm import palmChat
import documents as documents
import time

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
verifier = SignatureVerifier(os.environ['SIGNING_SECRET'])

app = App(token=os.environ["SLACK_BOT_TOKEN"])
handlers = Handlers()

BOT_ID = client.api_call('auth.test')['user_id']
print("bot id", BOT_ID)

start = {}
welcome_message_list = {}

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
    user_input = payload.get('text')
    ts = payload.get('ts')
    print("user id ", user_id)

    if user_id is not None and BOT_ID != user_id:

        if user_id not in start:
            start[user_id] = False

        if start[user_id] is True:
            client.reactions_add(name="speech_balloon", channel=channel_id, timestamp=ts)
            
            temp = thermos.get_temperature()

            if not DocumentsHandler.check_user_id_exists(user_id):
                new_document = {
                    'user_id': user_id,
                    'catalogs': [{'conversation': []}]
                }
                DocumentsHandler.create_document(new_document)

            document = DocumentsHandler.get_document_by_user(user_id)
            conversation_list = document['catalogs'][-1]['conversation']

            chat = palmChat(user_id, start[user_id], temp, user_input)
            response = str(chat)

            conversation_list.append({'user': user_input, 'bot': response})

            DocumentsHandler.update_document(user_id, document)

            client.chat_postMessage(channel=channel_id, text=response)

        time.sleep(1)
            
@app.action("creative_tone")
def creative_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_creative_tone(ack, body, logger)
    global thermos
    thermos = thermos.change_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to Creative!\nPlease ask away: ")

@app.action("balanced_tone")
def balanced_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_balanced_tone(ack, body, logger)
    global thermos
    thermos = thermos.change_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to Balanced!\nPlease ask away: ")

@app.action("precise_tone")
def precise_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_precise_tone(ack, body, logger)
    global thermos
    thermos = thermos.change_temperature(temperature)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to Precise!\nPlease ask away: ")

@app.event("reaction_added")
def reaction(payload):
    user_id = payload.get('user')
    channel_id = payload.get('item',{}).get('channel')

    if f'@{user_id}' not in welcome_message_list:
        return
    
    welcome = welcome_message_list[f'@{user_id}'][user_id]
    welcome.completed = True
    welcome.channel = channel_id
    message = welcome.get_message()
    updated_message = client.chat_update(**message)
    welcome.timestamp = updated_message['ts']

@app.event("app_home_opened")
def open_home(client,event,logger):
    home_display = HomeDisplay(client,event,logger)
    home_display.display_home()

@app.command('/start')
def handle_start(ack, body, logger):
    ack()
    logger.info(body)
    user_id = body['user_id']

    if user_id not in welcome_message_list:
        welcome_message_list[user_id] = {}

    if user_id not in start:
        start[user_id] = False

    channel_id = body['channel_id']
    tone_button_block = TONE_BUTTON_BLOCK
    client.chat_postMessage(channel=channel_id, blocks=tone_button_block["blocks"])

    if not DocumentsHandler.check_user_id_exists(user_id):
        new_document = {
            'user_id': user_id,
            'catalogs': [{'conversation': []}]
        }
        DocumentsHandler.create_document(new_document)

    start[user_id] = True
    chat = palmChat(user_id, start[user_id], thermos.get_temperature(), '')
    client.chat_postMessage(channel=channel_id, text=chat.response)

    print(f'/start status, {start.get_status()}')

@app.command('/quit')
def handle_quit(ack, body, logger):
    ack()
    logger.info(body)
    user_id = body['user_id']
    channel_id = body['channel_id']

    if user_id in start:
        start[user_id] = False

    client.chat_postMessage(channel=channel_id, text="You have quit the conversation")

    if DocumentsHandler.check_user_id_exists(user_id):
        document = DocumentsHandler.get_document_by_user(user_id)
        document['catalogs'].append({'conversation': []})
        DocumentsHandler.update_document(user_id, document)

    print(f'/quit status, {start.get(user_id)}\nTemperature, {thermos.get_temperature()}')

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()



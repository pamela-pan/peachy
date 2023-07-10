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

# chat_object = palm_chat.palmChat(temp=0.7, status=False)
# print('chat_object status: ', chat_object.get_status())
# print('chat_object temp: ', chat_object.get_temperature())
# global temperature
# temperature = 0.7 # default temp

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
    print("message works")
    user_id = payload.get('user')
    channel_id = payload.get('channel')
    text = payload.get('text')
    print(text)

    if user_id != None and BOT_ID != user_id:
        if text == 'list 5 fruits. limit your response to 5 words.':
            client.chat_postMessage(channel=channel_id, text=palm_chat.palmChat.start_chat(user_input=text))

@app.action("creative_tone")
def creative_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_creative_tone(ack, body, logger)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {temperature}!\nPlease ask away: ")

@app.action("balanced_tone")
def balanced_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_balanced_tone(ack, body, logger)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {temperature}!\nPlease ask away: ")

@app.action("precise_tone")
def precise_tone_action_wrapper(ack, body, logger):
    channel_id = body['container']['channel_id']
    temperature = handlers.handle_precise_tone(ack, body, logger)
    client.chat_postMessage(channel=channel_id, text=f"Your tone has been set to {temperature}!\nPlease ask away: ")

@app.event("reaction_added")
def reaction(payload):
    user_id = payload.get('user')
    channel_id = payload.get('item',{}).get('channel')
    # text = payload.get('text')

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
# boolean statement for bot_status
def go_online():
    return True

@app.command('/start')
def handle_start(ack, body, logger):
    ack()
    logger.info(body)
    channel_id = body['channel_id']
    tone_button_block = TONE_BUTTON_BLOCK
    client.chat_postMessage(channel=channel_id, blocks=tone_button_block["blocks"])
    print('handle_start has started', go_online())
    # palm_chat.palmChat(get_temp(), go_online())
    # print()
    # turns bot on
    # print(palm_chat.palmChat.status_listener())
    # a.listen(status = bot_status) # call listen
    # a.chat() #call chat
    
    # palm_status = palm_chat.palmChat.listen(bot_status)

# @app.event('message')
# def listen_user_input(payload):
#     if 

# --------- PALM CODE ----------



if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()



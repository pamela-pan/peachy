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

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
verifier = SignatureVerifier(os.environ['SIGNING_SECRET'])

app = App(token=os.environ["SLACK_BOT_TOKEN"])
handlers = Handlers()

BOT_ID = client.api_call('auth.test')['user_id']
print("bot id", BOT_ID)

welcome_message_list ={}

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

    if user_id != None and BOT_ID != user_id:
        if text == 'start':
            # send_welcome_message(channel_id, user_id) # any channel
            send_welcome_message(f'@{user_id}', user_id) # dm
        if text == 'tone':
            print("tone buttons working")
            tone_button_block = TONE_BUTTON_BLOCK
            client.chat_postMessage(channel=channel_id, blocks=tone_button_block["blocks"])
            
# tonality buttons
temperature = 0.7 # default temp

@app.action("creative_tone")
def creative_tone_action_wrapper(ack, body, logger):
    temperature = handlers.handle_creative_tone(ack, body, logger)
    print(temperature)
    return temperature

@app.action("balanced_tone")
def balanced_tone_action_wrapper(ack, body, logger):
    temperature =  handlers.handle_balanced_tone(ack, body, logger)
    print(temperature)
    return temperature

@app.action("precise_tone")
def precise_tone_action_wrapper(ack, body, logger):
    temperature =  handlers.handle_precise_tone(ack, body, logger)
    print(temperature)
    return temperature


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




if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()



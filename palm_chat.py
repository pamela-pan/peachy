import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm
from pymongo import MongoClient

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
palm.configure(api_key=os.environ['PALM_API_KEY'])
model_list = [_ for _ in palm.list_models()]
model_id = 'models/text-bison-001'

class palmChat:
    prompt_number = 0
    catalog = {}

    def __init__(self, temp, status, user_input):
        self.temp = temp
        self.status = status
        self.user_input = user_input

        self.examples = [
                ("What's up?", "I'm great, how may I help you?"),
                ("Hi", "Hey! How can I help you."),
                ("Hey", "Hi there, how may I assist you?"),
                ("Thank you", "You're welcome!")
            ]
        
        self.completion = palm.generate_text(
                        model=model_id,
                        prompt=self.get_history() + self.get_user_message(),
                        temperature=self.get_temperature(),
                        max_output_tokens=1000,
                        candidate_count=1
                    )
        
        self.palm_response = self.get_palm_response()
        self.update_catalog()
        self.update_prompt_number()
        self.get_current_conversation()

        print(self.get_current_catalog())

    def get_status(self):
        return self.status
        
    def get_temperature(self):
        return self.temp
    
    def get_user_message(self):
        return self.user_input
    
    def get_history(self):
        if len(palmChat.catalog) < 1:
            history = ""
        else:
            history = palmChat.catalog['convo_0']['bot']
        return history
    
    def get_palm_response(self):
        response = palm.chat(
                context="Be an informative assistant that is clear and concise. Be straight to the point, and dont over explain things.",
                examples=self.examples,
                messages=self.get_history() + self.get_user_message()
            )
        bot_output = response.candidates[0]['content']
        return bot_output
    
    def get_current_catalog(self):
        return palmChat.catalog
    
    def get_current_conversation(self):
        # print("current catalog ", self.get_current_catalog())
        # print("current index ", palmChat.prompt_number)
        current_convo_key = str(f"convo_{palmChat.prompt_number -1}")
        # print("current convo value ",palmChat.catalog[current_convo_key])
        current_conversation = {current_convo_key: palmChat.catalog[current_convo_key]}
        # print("current convo ", current_conversation)
        return(current_conversation)

    def create_new_conversation(self):
        conversation = {'user': '', 'bot': ''}
        conversation['user'] = self.get_user_message()
        conversation['bot'] = self.palm_response
        return conversation
    
    def conversation_name(self):
        number = str(f"convo_{palmChat.prompt_number}")
        return number
    
    def update_prompt_number(self):
        palmChat.prompt_number += 1
    
    def update_catalog(self):
        self.get_current_catalog()[self.conversation_name()] = self.create_new_conversation()
        # print('updated, ', self.get_current_catalog())


    

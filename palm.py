import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm
from pymongo import MongoClient
from documents import DocumentsHandler

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
palm.configure(api_key=os.environ['PALM_API_KEY'])
model_list = [_ for _ in palm.list_models()]
model_id = 'models/text-bison-001'

class palmChat():
    def __init__(self, user_id, user_status, temp, user_input=''):
        self.user_id = user_id
        self.status = user_status
        self.temp = temp
        self.user_input = user_input
        self.examples = [
            ("This is context from a previous conversation: (user:'list five fruits', bot:'apple, banana, mango, pineapple, orange'). Use this context to help your response to the following message if it applies: what is the first item in the list?", "Apple"),
            ("This is context from a previous conversation: (user:'', bot:''). Use this context to help your response to the following message if it applies: what is the first item in the list?", "Sorry, I didn't get that. Would you like me to list some items for you?"),
            ("This is context from a previous conversation: (user:'what is the first item in the list?', bot:'Sorry, I didn't get that. Would you like me to list some items for you?'). Use this context to help your response to the following message if it applies: yes", "Sure, here is a random list of five countries: Guadamala, New Zealand, Australia, Greenland, Canada"),
            ("This is context from a previous conversation: (user:'56+44', bot:'100'). Use this context to help your response to the following message if applies: my bad, i didnt mean that, i meant to say minus", "No worries, 56 - 44 = 12")
        ]
        self.response = self.palm_response()

    def palm_response(self):
            response = palm.chat(
                context='Be an informative assistant, be direct, not too friendly but still helpful.',
                examples=self.examples,
                messages=str(self.previous_dialouge()+self.user_input),
                temperature=self.temp,
            )
            output = response.candidates[0]['content']
            self.update_conversations(output)
            return output
        
    def previous_dialouge(self):
        document = DocumentsHandler.get_document_by_user(self.user_id)
        if len(document['catalogs'][-1]['conversation']) < 1:
            context = '(user:'', bot:'')'
        else: 
            context = str("This is context from a previous conversation: " + f"(user:'{document['catalogs'][-1]['conversation'][-1]['user']}', bot:'{document['catalogs'][-1]['conversation'][-1]['bot']}'). " + "Use this context to help responond to the following message if you think it applies: ")
        return context

    def update_conversations(self, response):
        document = DocumentsHandler.get_document_by_user(self.user_id)
        if document is not None:
            if not document['catalogs']:
                document['catalogs'].append({'conversation': []})
            document['catalogs'][-1]['conversation'].append({'user': self.user_input, 'bot': response})
            DocumentsHandler.update_document(self.user_id, document)
        else:
            print(f"User with user_id '{self.user_id}' not found in the database.")

    def update_catalogs(self):
        document = DocumentsHandler.get_document_by_user(self.user_id)
        if document is not None:
            document['catalogs'].append({'conversation': []})
            DocumentsHandler.update_document(self.user_id, document)
        else:
            print(f"User with user_id '{self.user_id}' not found in the database.")

    def __str__(self):
        return self.response

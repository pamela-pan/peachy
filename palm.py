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
            ('hi', 'Hi, how may I help you?'),
            ('hey', 'Hi, how can I assist you?')
        ]
        self.response = self.palm_response()

    def palm_response(self):
        if self.user_input == 'create a new catalog':
            output = 'A new catalog has been created.'
            self.update_catalogs()
            return output
        else:
            response = palm.chat(
                context='Informative Assistant',
                examples=self.examples,
                messages=self.user_input,
                temperature=self.temp
            )
            output = response.candidates[0]['content']
            self.update_conversations(output)
            return output

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

import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm
import documents

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
palm.configure(api_key=os.environ['PALM_API_KEY'])
model_list = [_ for _ in palm.list_models()]
model_id = 'models/text-bison-001'

class palmChat:
    prompt_number = 1
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
                        max_output_tokens=500,
                        candidate_count=1
                    )
        
        self.fill_catalog()

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
            history = palmChat.catalog['convo1']['bot']
        return history
    
    def get_palm_response(self):
        response = palm.chat(
                context="Be an informative assistant that is clear and concise. Be straight to the point, and dont over explain things.",
                examples=self.examples,
                messages=self.get_history() + self.get_user_message()
            )
        bot_output = response.candidates[0]['content']
        return bot_output
    
    def upload_current_catalog(self):
        catalog_id = documents.insert_catalog(palmChat.catalog)
        # print("this is catalog id", catalog_id)
        return catalog_id


    def fill_catalog(self):
        convo_number = str(f"convo{palmChat.prompt_number}")
        palmChat.catalog[convo_number] = {'user': '', 'bot': ''}
        palmChat.catalog[convo_number]['user'] = self.get_user_message()
        palmChat.catalog[convo_number]['bot'] = self.get_palm_response()
        res = {f"{convo_number}":  palmChat.catalog[convo_number]}
        palmChat.prompt_number += 1
        return res

    def upload_current_conversation(self):
        documents.update_catalog()

    
a = palmChat(0.7, True, "what is tulip")
# print(type(a))
print("this is catelog id",a.upload_current_catalog())

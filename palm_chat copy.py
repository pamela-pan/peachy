import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
palm.configure(api_key=os.environ['PALM_API_KEY'])
model_list = [_ for _ in palm.list_models()]
model_id = 'models/text-bison-001'

class palmChat:
    temperature = 0.7 # default temp
    prompt_number = 0
    catalog = {}

    def __init__(self, temp):
        self.temp = temp
    def chat(self, user_input):
        
        while True:
            if len(palmChat.catalog) < 1:
                history = ""
            else:
                history = palmChat.catalog['convo0']['bot']

            examples = [
                ("What's up?", "I'm great, how may I help you?"),
                ("Hi", "Hey! How can I help you."),
                ("Hey", "Hi there, how may I assist you?"),
                ("Thank you", "You're welcome!")
            ]
            
            completion = palm.generate_text(
                        model=model_id,
                        prompt=history + user_input,
                        temperature=self.temp,
                        max_output_tokens=500,
                        candidate_count=1
                    )

            response = palm.chat(
                context="Be an informative assistant that is clear and concise. Be straight to the point, and dont over explain things.",
                examples=examples,
                messages=history + user_input
            )
            
            response_text = response.candidates[0]['content']
            bot_output = ('Response:\n '  + str(response_text))

            print(bot_output)
            print('-'*50)

            convo_number = str(f"convo{palmChat.prompt_number}")
            palmChat.catalog[convo_number] = {'user': '', 'bot': ''}
            palmChat.catalog[convo_number]['user'] = user_input
            palmChat.catalog[convo_number]['bot'] = bot_output

            palmChat.prompt_number += 1

    def __str__(self):
        print("palm chat temp",self.temp)
        return str(self.temp)
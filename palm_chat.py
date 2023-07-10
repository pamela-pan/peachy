import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm
import bot

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
palm.configure(api_key=os.environ['PALM_API_KEY'])
model_list = [_ for _ in palm.list_models()]
model_id = 'models/text-bison-001'

class palmChat:
    prompt_number = 0
    catalog = {}

    def __init__(self, temp=0.7, status=False, user_input=''):
        self.temp = temp
        self.status = status
        self.user_input = user_input

    def get_status(self):
        return self.status
        
    def get_temperature(self):
        return self.temp
        
    # user_input is type string
    def start_chat(self):
        # print("user_input ", self.user_input)
        # if palmChat.listen() == True:
        # return b
        while bot.go_online():
            if len(palmChat.catalog) < 1:
                history = ""
            else:
                history = palmChat.catalog['convo0']['bot']

            # user input is reset every time a user types

            examples = [
                ("What's up?", "I'm great, how may I help you?"),
                ("Hi", "Hey! How can I help you."),
                ("Hey", "Hi there, how may I assist you?"),
                ("Thank you", "You're welcome!")
            ]
            
            completion = palm.generate_text(
                        model=model_id,
                        prompt=history + self.user_input,
                        temperature=self.temp,
                        max_output_tokens=500,
                        candidate_count=1
                    )

            response = palm.chat(
                context="Be an informative assistant that is clear and concise. Be straight to the point, and dont over explain things.",
                examples=examples,
                messages=history + self.user_input
            )
            
            bot_output = response.candidates[0]['content']

            convo_number = str(f"convo{palmChat.prompt_number}")
            palmChat.catalog[convo_number] = {'user': '', 'bot': ''}
            palmChat.catalog[convo_number]['user'] = self.user_input
            palmChat.catalog[convo_number]['bot'] = bot_output

            palmChat.prompt_number += 1
            return bot_output

    # def __str__(self):
    #     print("string method ",str(self.status))
    #     return self.status
    
# a = palmChat(0.4, False)
# print('temperature = ', a.get_temperature())
# a.set_status(True)
# print('getting the current status: ', a.get_status())

# print('setting the status to: ', a.set_status(True))
# print(a.start_chat('list 5 fruits. limit your response to 5 words'))
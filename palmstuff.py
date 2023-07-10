import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

palm.configure(api_key=os.environ['PALM_API_KEY'])

model_list = [_ for _ in palm.list_models()]
# for model in model_list:
#     print(model.name)

model_id = 'models/text-bison-001'

prompt_number = 0
catalog = {}

# Returns a specific conversation from the catalog, a is a string
def get_conversation(a):
    return catalog[a]


while True:
    if len(catalog) < 1:
        history = ""
    else:
        history = catalog['convo0']['bot']

    user_input = input('Prompt: ')
    if user_input == 'quit':
        break
    if user_input == 'hello':
        print('hey')
    examples = [
        ("What's up?", "I'm great, how may I help you?"),
        ("Hi", "Hey! How can I help you."),
        ("Hey", "Hi there, how may I assist you?"),
        ("Thank you", "You're welcome!")
    ]

    completion = palm.generate_text(
                model=model_id,
                prompt=history + user_input,
                temperature=0.6,
                max_output_tokens=500,
                candidate_count=1
            )
    
    print(completion)

    response = palm.chat(
        context="Be an informative assistant that is clear and concise. Be straight to the point, and dont over explain things.",
        examples=examples,
        messages=history + user_input
    )
    
    response_text = response.candidates[0]['content']
    bot_output = ('Response:\n '  + str(response_text))

    print(bot_output)
    print('-'*50)

    convo_number = str(f"convo{prompt_number}")
    catalog[convo_number] = {'user': '', 'bot': ''}
    catalog[convo_number]['user'] = user_input
    catalog[convo_number]['bot'] = bot_output

    prompt_number += 1

print(get_conversation('convo0'))
print(catalog)
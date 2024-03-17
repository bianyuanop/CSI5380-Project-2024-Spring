import re
from string import Formatter
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

intents = {
    'check-weather': {
        'desc': 'fill when user want to know how\'s the weather',
        'slots':  {
            'location': 'location to check weather'
        },
        'response-template': '''USER: You are a helpful, virtual assistant. Always answer as helpfully as possible. 
Here user want to check weather of {location}, and now the temperature of {location} is {temperature}.
Please answer briefly the temperature of {location}.
ASSISTANT:'''
    },
    'open-youtube': {
        'desc': 'fill when user want to watch youtube',
        'slots':  {
            'video': 'the video description user would like to watch'
        },
        'response-template': '''USER: You are a helpful, polite, virtual assistant. Always answer as helpfully as possible. 
Here user want to watch a video, and you have requested the operating system to open youtube website, the response from the operating system is: {video_open_result}
Please answer if you have opened the youtube video or not.
ASSISTANT:'''
    },
    'play-music': {
        'desc': 'fill when user want to listen music',
        'slots': {
            'author': 'author of the music',
            'music': 'music user want to listen'
        },
        'response-template': '''USER: You are a helpful, polite, virtual assistant. Always answer as helpfully as possible. 
Here user want to listen music, and you have requested the operating system to open music app, the response from the operating system is: {music_open_result}
Please answer if you have started playing the music the user requested.
ASSISTANT:'''
    },
    'open-app': {
        'desc': 'fill when user want to open application, application list: music, phone, telegram' ,
        'slots': {
            'application': 'the application user want to open'
        },
        'response-template': '''USER: You are a helpful, polite, virtual assistant. Always answer as helpfully as possible. 
Here user want to open application {app}, and you have requested the operating system to open this app, the response from the operating system is: {open_result}
Please answer if you have opened the app or not.
ASSISTANT:'''
    },
    'OOS': {
        'desc': 'fill only when other intents are not seem correct to fill',
        'slots': {}
    }
}

def intents_to_string(intents: dict):
    res = ""
    i = 1
    for k, v in intents.items():
        intent = k
        desc = v['desc']
        slots = v['slots']
        res += f'{i}. {intent}\n'
        for slot_name in slots: 
            slot_desc = slots[slot_name]

            res += f'\t{slot_name}:{slot_desc}\n'
        i += 1

    return res

template = """
USER: You are a helpful, virtual assistant.  Please always answer in the following template: 
User Intent: <intent>
Slots:
<slot-1 name>:<slot-1 content>
<slot-2 name>:<slot-2 content>
...
<slot-n name>:<slot-n content>

Intent name, description and corresponding slots information are given below:
""" + intents_to_string(intents) + """
If no intention is found in the above list, please simply label User Intent to `OOS`

Here's one example of answering:
when user say: "What's the weather today in Ottawa?"
you should answer following:
User Intent:check-weather
Slots:
location:Ottawa

ASSISTANT: Ok great ! I will reply in such format
USER: {question}
ASSISTANT:
"""

def extract_intention_and_slots(response: str):
    p = re.compile('User Intent:.*')
    m = p.search(response)
    if m == None:
        raise Exception("unable to match intent")

    intent = m[0].split(':')[-1].strip().lstrip()
    print(f'intent: {intent}')
    if intent not in intents:
        raise Exception("no such intent defined")

    slots = {}
    for slot_name in intents[intent]['slots']:
        sp = re.compile(f'{slot_name}:.*') 
        m = sp.search(response)
        if m == None:
            slots[slot_name] = 'N/A'
            continue
        
        slots[slot_name] = m[0].split(':')[-1].lstrip().strip()

    return {
        'intent': intent,
        'slots': slots
    }

def _get_slots2format(s: str):
    slots = [fn for _, fn, _, _ in Formatter().parse(s) if fn is not None]
    slots = list(set(slots))

    return slots
 

def gen_response(intent: str, params: dict):
    if intent not in intents:
        return "Sorry, we cannot process your command."
    

    param_names = _get_slots2format(intents[intent]['response-template']) 
    print(params.keys())
    print(param_names)


    prompt = PromptTemplate(template=intents[intent]['response-template'], input_variables=param_names)
    llm = OpenAI(openai_api_base="https://api.openai.com/v1")
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.invoke(input=params)['text']
    # run(**params)

    return result


if __name__ == "__main__":
    response = '''
User Intent:check-weather
Slots:
location:Ottawa
    '''

    print(extract_intention_and_slots(response))
import os
import dotenv
import gradio as gr
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import actions
import intent

def audio_to_text(audio):
    return "How's the weather today in Ottawa"

def detect_intent_slots_filling(question: str):
    prompt = PromptTemplate(template=intent.template, input_variables=["question"])
    llm = OpenAI(openai_api_base="https://api.openai.com/v1")
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.invoke({
        'question': question
    })['text']
    # run(question=question)

    intention = intent.extract_intention_and_slots(result) 

    return intention

def trigger_action_response_gen(intention) -> str:
    _intent = intention['intent']
    slots = intention['slots']
    print(f'intent: {_intent}, slots: {slots}')

    if _intent == 'check-weather':
        temp = actions.check_weather(slots['location'])
        print(temp)

        response_text = intent.gen_response(_intent, {
            'location': slots['location'],
            'temperature': temp
        })

        print(f'responding user with: {response_text}')

        return response_text
    else:
        return "Sorry, I do not understant. Can you repeat again"

def tts(text):
    pass


if __name__ == '__main__':
    dotenv.load_dotenv(override=True)
    q = audio_to_text('')
    it = detect_intent_slots_filling(q)
    resp = trigger_action_response_gen(it)
    tts(resp)


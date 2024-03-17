import io
import os
import dotenv
import requests
import numpy as np
import gradio as gr
import base64
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from scipy.io import wavfile
import soundfile
import json
import actions
import intent

dotenv.load_dotenv(override=True)
whisper_host = os.environ['WHISPER_HOST']
tts_host = os.environ['TTS_HOST']

def audio_to_text(audio):
    sr: int = audio[0]
    data: np.ndarray = audio[1]

    bytes_wav = bytes()
    f = io.BytesIO(bytes_wav)
    wavfile.write(f, sr, data)

    files = {
        'audio_file': f
    }

    url = os.path.join(whisper_host, 'asr')
    resp = requests.post(url, headers={
        'accept': 'application/json'
    }, params={
        'encode': True,
        'task': 'transcribe',
        'language': 'en',
        'output': 'txt'
    }, files=files)

    print(resp.text)

    return resp.text

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
        return "Sorry, I don't understant. Can you repeat again"

def tts(text: str):
    sid = 22
    resp = requests.post(tts_host + '/tts', data={
        "text": text,
        "sid": sid
    })

    audiob64 = json.loads(resp.text)['audio']
    audio_bytes = base64.b64decode(audiob64)
    audio_file = io.BytesIO(audio_bytes)
    audio_file.seek(0)
    audio, sr = soundfile.read(audio_file)

    return sr, audio

def main(audio):
    q = audio_to_text(audio) 
    it = detect_intent_slots_filling(q)
    resp = trigger_action_response_gen(it)
    return tts(resp)

if __name__ == '__main__':
    app = gr.Interface(
        main,
        gr.Audio(sources=['microphone', 'upload']),
        gr.Audio()
    )

    app.launch()

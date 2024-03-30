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

    response_text = "Sorry, I don't understand. Can you repeat again"
    if _intent == 'check-weather':
        temp = actions.check_weather(slots['location'])
        print(temp)

        response_text = intent.gen_response(_intent, {
            'location': slots['location'],
            'temperature': temp
        })
    elif _intent == 'open-youtube':
        video = actions.open_youtube(slots['video'])
        print(video)
        video_open_result = f"opened video `{video['title']}` at youtube"

        response_text = intent.gen_response(_intent, {
            'video_open_result': video_open_result            
        })
    elif _intent == 'play-music':
        music = actions.play_music(slots['author'], slots['music'])
        music_open_result = f"played music `{music['music']}` by `{music['author']}` for you"
        print(music_open_result) 
        response_text = intent.gen_response(_intent, {
            'music_open_result': music_open_result            
        })
    elif _intent == 'open-app':
        app = actions.open_app(slots['application']) 
        open_result = f"opened app `{app}`"
        response_text = intent.gen_response(_intent, {
            'app': app,
            'open_result': open_result
        })
    else:
        response_text = "Sorry, I don't understand. Can you repeat again"

    print(f'responding user with: {response_text}')
    return response_text

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

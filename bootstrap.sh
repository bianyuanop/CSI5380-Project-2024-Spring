#!/usr/bin/bash

WHISPER_DIR="whisper-asr-webservice"
TTS_DIR="GanyuTTS"

cd $WHISPER_DIR
echo "launching whisper"
docker run -d --gpus all -p 19000:9000 -e ASR_MODEL=base -e ASR_ENGINE=openai_whisper onerahmet/openai-whisper-asr-webservice:latest-gpu
cd $TTS_DIR
echo "launching GanyuTTS"
docker compose up -d

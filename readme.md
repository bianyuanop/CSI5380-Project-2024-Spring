## Prequisites

+ Docker >=24
+ GPU with at least 4.5GB of RAM
+ Python >= 3.10

Run following commands before you go

```shell
python3 -m venv .venv
pip install -r requirements.txt
source .venv/bin/activate
```

## Start

Simply run 

```
python main.py
```

## Bootstrapping dependent TTS and audio to text services

First you need to fill your OPENAI key in file `.env.example`, then move this file to `.env`. 

Then simply run

```bash
./bootstrap.sh
```

Note that since there is an unsolved issue in dockerized `GanyuTTS`, so after you launching up the docker instance of that, you need to bash into the `GanyuTTS` container and replace the function `tts` at `/opt/GanyuTTS/api.py` to this:

```python
@app.route('/tts', methods=['POST'])
def tts():
    start = time.time()
    text = request.form.get('text')
    # get sid too, but only if it's provided
    if 'sid' in request.form:
        sid = int(request.form.get('sid'))
    else:
        sid = 22

    sid2 = None
    if 'sid2' in request.form:
        sid2 = str(request.form.get('sid2'))

    print("Got text from client: " + text)

    audio, sr = generate_VITS(text, sid)
    if sid2 != None:
        audio, sr = generate_SO_VITS(audio, sr, sid2)

    file_object = io.BytesIO()
    soundfile.write(file_object, audio, sr, format="wav")
    file_object.seek(0)
    file_string = file_object.read()
    audio = base64.b64encode(file_string).decode('utf-8')
    print("Done in " + str(time.time() - start) + " seconds")
    return jsonify({'audio': audio})
```

Then restart the container
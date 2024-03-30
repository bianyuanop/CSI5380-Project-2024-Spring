import os
import subprocess
import threading

def check_weather(location: str):
    degree = {
        'Ottawa': '10C',
        'Toronto': '20C',
        'Califolia': '25C'
    }

    if location not in degree:
        return 'Err: no such location in db'
    
    return degree[location]

def open_youtube(video_desc: str):
    videos = [
        {
            'title': 'virtual assitant best practice in Python',
            'link': 'http://youtube.com/someid',
            'desc': 'this video elucidates how to make a virtual assistant in Python'
        } 
    ]

    # Search operations 

    return videos[0]

def play_music(author: str, music: str):
    musics = [
        {
            'author': 'The Weeknd',
            'music': 'Blinding Lights'
        }
    ] 

    # Search operations

    return musics[0]

def open_app(app: str):
    apps = [
        {
            'name': 'discord',
            'handlerFn': open_discord
        }
    ]

    matches = [i for i in apps if i['name'] == app.lower()]
    if len(matches) == 0:
        return 'Err: app not exists'
    
    fn = matches[0]['handlerFn']
    app_starter = threading.Thread(target=fn, name=matches[0]['name'])
    app_starter.start()

    return apps[0]

def open_discord() -> bool:
    sub = run_command(['discord'])
    if sub.returncode != 0:
        return False
    
    return True

def run_command(args, check=True, shell=False, cwd=None, env=None, timeout=None, capture_output=False): 
    env = env if env else {} 
    return subprocess.run( 
        args, 
        check=check, 
        shell=shell, 
        capture_output=capture_output, 
        env={ 
            **os.environ, 
            **env 
        }, 
        cwd=cwd, 
        timeout=timeout 
    ) 
import os
import subprocess
import threading
import webbrowser

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
            'title': 'Python Tutorial - Python Full Course for Beginners',
            'link': 'https://youtu.be/_uQrJ0TkZlc?si=Fa4XsqgwnhPKMW7F',
            'desc': '''Become a Python pro! 🚀 This comprehensive tutorial takes you from beginner to hero, covering the basics, machine learning, and web development projects.
🚀 Want to dive deeper?
- Check out my Python mastery course: https://bit.ly/434YnGt
- Subscribe for more awesome Python content: https://goo.gl/6PYaGF
'''
        },
    ]

    # TODO: Search operations 
    webbrowser.open(videos[0]['link'])

    return videos[0]

def play_music(author: str, music: str):
    musics = [
        {
            'author': 'Dawid Podsiadło',
            'music': 'Let You Down',
            'link': 'https://youtu.be/BnnbP7pCIvQ?si=IfjrUvuEWaKUMPfp',
        },
        {
            'author': 'ARIANNE',
            'music': 'KOMM, SUSSER TOD',
            'link': 'https://youtu.be/hoKluzn07eQ?si=BrR7LTOafeCRdG3p'
        },
        {
            'author': 'ARIANNE',
            'music': 'Midnight City',
            'link': 'https://youtu.be/dX3k_QDnzHE?si=LQRAAJxU2Gz1Fjsf'
        },
    ] 

    webbrowser.open(musics[0]['link'])

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

def open_website(url: str):
    pass

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
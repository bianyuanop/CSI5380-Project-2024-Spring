def check_weather(location: str):
    degree = {
        'Ottawa': '10C'
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
            'author': 'Jay Chou',
            'music': 'xxx'
        }
    ] 

    # Search operations

    return musics[0]

def open_app(app: str):
    apps = [
        {
            'name': 'discord',
            'handlerFn': lambda: print('opening discord')
        }
    ]

    # Search operations

    return apps[0]
'''
on  :  2019-07-10
by  :  Kris Huang

for : init data formater of other paltforms

'''

import json
import os.path


def initprasers():
    music_ = './music.platform.json'
    if os.path.isfile(music_):
        print('loading music platforms parser')
        with open(music_, 'r') as f:
            musicPlatforms = json.load(f)
            print(list(musicPlatforms.keys()))

 initprasers()
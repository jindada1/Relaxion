'''

    integrate all functional modules and services into views instance

    return views instance out

'''
import json
from views import *
from db import *
from platforms import *
from core import *

def register_services():

    with open('./config.json', 'r') as f:
        cfg = json.loads(f.read())
        
        platforms_cfg = cfg['platforms']
        dbpath = cfg['database']['path']
        ffmpegpath = cfg['core-extract']["ffmpeg-path"]
        mediafolder = cfg['mediafolder']["path"]

        parser = PraserService(platforms_cfg)
        extractor = Extractor(ffmpegpath, mediafolder)
        dolder = Downloader(mediafolder)
        localdb = dbService(dbpath)

        return (
            Cores([extractor, dolder]),
            Users([localdb]),
            Platforms([parser])
        )
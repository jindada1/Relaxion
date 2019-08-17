'''
on  :  2019-07-10
by  :  Kris Huang

for : init data formater of other paltforms
'''

from .qqmusic import QQparser
from .wangyimusic import WangYiparser
from .kugoumusic import KuGouparser

import json

class PraserService(object):
    def __init__(self, cfg):
        self.platforms = {}
        
        # no outer settings, read local default setting
        if not cfg:
            with open('./settings/platforms.json', 'r') as f:
                content = f.read()
                cfg = json.loads(content)


        for name, prop in cfg.items():
            # we can validate the target url here
            # '''
            # construct instance according to cfg
            constructor = globals()[prop['parser']]
            instance = constructor(prop['target'])
            self.platforms[name] = instance
    
    # override [], return parser
    def __getitem__(self, key):

        if key in self.platforms.keys():
            return self.platforms[key]

        return None

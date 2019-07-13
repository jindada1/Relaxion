'''
on  :  2019-07-10
by  :  Kris Huang

for : init data formater of other paltforms
'''

from platforms import *
import json

class PraserService(object):
    def __init__(self, cfg):
        self.platforms = {}
        # no outer settings, read local default setting
        if not cfg:
            try:
                with open('./settings/platform_setting.json', 'r') as f:
                    content = f.read()
                    cfg = json.loads(content)
            except:
                print("setting file error")
                return

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



othercfg = {}
superParser = PraserService(othercfg)
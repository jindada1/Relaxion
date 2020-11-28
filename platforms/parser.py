'''
on  :  2019-07-10
by  :  Kris Huang

for : init data formater of other paltforms
'''

from .qq import QQ
from .wangyi import WangYi
from .kugou import KuGou
from .youku import YouKu
from .migu import MiGu
from .kuwo import KuWo

class PraserService(object):
    def __init__(self, cfg):
        self.platforms = {}
        
        if not cfg:
            print('[-] no platform service was registered')

        for name, prop in cfg.items():
            # we can validate the third url here
            # '''
            # construct instance according to cfg
            constructor = globals()[prop['parser']]
            instance = constructor(prop['third'])
            self.platforms[name] = instance
    
    # override [], return parser
    def __getitem__(self, key):

        if key in self.platforms.keys():
            return self.platforms[key]

        return None

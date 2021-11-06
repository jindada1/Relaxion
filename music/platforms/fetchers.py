'''
on  :  2019-07-10
by  :  Kris Huang
'''

from .qq import QQ
from .wangyi import WangYi
from .kugou import KuGou
from .migu import MiGu
from .kuwo import KuWo

class Fetchers(object):
    def __init__(self, cfg):
        self.platforms = {}
        
        if not cfg:
            print('[-] no platform service was registered')

        for name, prop in cfg.items():
            # construct instance according to cfg
            constructor = globals()[prop['fetcher']]
            instance = constructor()
            self.platforms[name] = instance
    
    # override [], return fetcher
    def __getitem__(self, key):

        if key in self.platforms.keys():
            return self.platforms[key]

        return None

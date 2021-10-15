'''
on  :  2019-09-26
by  :  Kris Huang

for : integrate functional operation modules to package -- "core"
'''

__all__ = ['Extractor', 'Downloader']
__version__ = '0.1'
__author__ = 'Kris Huang'


from .extractor import Extractor
from .downloader import Downloader

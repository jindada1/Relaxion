'''
on  :  2019-07-13
by  :  Kris Huang

for : integrate parser modules to package -- "platforms"
'''
from .baseparser import baseParser
from .qqmusic import QQparser
from .wangyimusic import WangYiparser


__all__ = ['baseParser','QQparser','WangYiparser']
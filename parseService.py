'''
on  :  2019-07-10
by  :  Kris Huang

for : init data formater of other paltforms

'''

from parsers.qqmusic import QQparser
from parsers.wangyimusic import WangYiparser


def initprasers():
    platforms = {
        "qq":QQparser("qq url"),
        "wangyi":WangYiparser("wangyi url")
    }

    return platforms


superParser = initprasers()
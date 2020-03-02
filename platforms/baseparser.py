'''
on  :  2019-07-11
by  :  Kris Huang

for : parse data from other platforms to the format of our platform
'''

# define data schema of our platform

from aiohttp import ClientSession
from datetime import datetime
import time
import json
import base64
import urllib


class Base(object):

    def __init__(self, **kwargs):

        third = kwargs["third"]
        name = kwargs["name"]
        
        self.thirdparty = third
        self.cookies = {}
        self.headers = {}

        if third:
            print("[ok] connect %s to third party server: %s" % (name, self.thirdparty))

        else:
            print("[ok] construct %s" % name)


    async def _asyncGetHeaders(self, url, params = None):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            return resp.headers

    async def _asyncGetText(self, url, params = None):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            return await resp.text()


    async def _asyncGetJson(self, url, params = None):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            return json.loads(await resp.text())


    async def _asyncPostJson(self, url, params = None, cookies = None):
        async with ClientSession(cookies = cookies) as session:
            resp = await session.post(url, data=params, headers=self.headers)
            return json.loads(await resp.text())


    async def _asyncGetJsonHeaders(self, url, params = None):
        async with ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                a = await resp.text()
                return json.loads(a)


    async def _asyncGetJsonHeadersCookies(self, url, params = None):
        async with ClientSession(cookies=self.cookies) as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                a = await resp.text()
                return json.loads(a)


    def jsonify(self, _dict):

        return json.dumps(_dict).replace(" ", '')


    def base64decode(self, text):
        
        return base64.b64decode(text).decode(encoding="utf-8-sig")

    def base64encode(self, text):

        return base64.b64encode(text)

    def to_time(self, timestamp):
        
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d, %H:%M:%S")

    @property
    def now_str(self):

        return str(int(time.time()))

    def quote_cna(self, val):
        if '%' in val:
            return val
        return urllib.parse.quote(val)

    def split_url(self, url):

        return urllib.parse.urlsplit(url)

    def unsplit_url(self, url):

        return urllib.parse.urlunsplit(url)
    


class Music(Base):

    def __init__(self, **kwargs):

        Base.__init__(self, **kwargs)

    def _getname(self, singers):
        artist = ""
        for index, singer in enumerate(singers):
            if index == 0:
                artist += singer['name']
            else:
                artist += "," + singer['name']
        return artist

    def _song(self, p, res_id, com_id, mv_id, pic_url, alb_name, lrc_url, name, arts, time, playable = True):
        return {
            "platform": p,
            "idforres": res_id,
            "url":'/{}/song/{}'.format(p, res_id),
            "idforcomments": com_id,
            "mvid": mv_id,
            "cover": pic_url,
            "albumname": alb_name,
            "lrc": lrc_url,
            "name": name,
            "artist": arts,
            "interval": time,
            "playable": playable
        }

    def _album(self, p, alb_id, pic_url, name, com_id, arts, pub_day):
        return {
            "platform": p,
            "albumid": alb_id,
            "pic_url": pic_url,
            "name": name,
            "idforcomments": com_id,
            "artist": arts,
            "publish_date": pub_day
        }

    def _mv(self, p, name, pic_url, mv_id, com_id, arts, time, pub_day):
        return {
            "platform": p,
            "name": name,
            "pic_url": pic_url,
            "mvid": mv_id,
            "idforcomments": com_id,
            "artist": arts,
            "duration": time,
            "publish_date": pub_day
        }

    def _uri(self, uri = None):
        if uri:
            return {"uri": uri}
        return {"uri": 'https://www.baidu.com', "error": 1}

    def _comment(self, avatar, username, content, stars, time):
        return {
            "avatar": avatar,
            "username": username,
            "content": content,
            "stars": stars,
            "time": time
        }

    def _songlist(self,p, _id, name, pic, songnum):
        return {
            "platform":p,
            "dissid":_id,
            "name": name,
            "pic": pic,
            "songnum": songnum
        }

    def mvpicCDN(self, path):
        # redirect to mv cover url
        return self.mv_pic_host + path

    async def searchSong(self, k, p, n):
        return "base search result"

    async def searchAlbum(self, k, p, n):
        return "base search result"

    async def searchMV(self, k, p, n):
        return "base search result"

    async def mvuri(self, _id):
        return "mvuri"

    async def musicuri(self, _id):
        return "musicuri"

    async def lyric(self, _id):
        return "lyric"

    async def songsinList(self, dissid, p, n):
        return "songsinList"

    async def songsinAlbum(self, _id):
        return "songsinAlbum"

class Video(Base):
    
    def __init__(self, **kwargs):

        Base.__init__(self, **kwargs)

    def search(self, _id):
        pass
    
    def videouri(self, _id):
        pass
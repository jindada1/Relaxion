'''
on  :  2019-07-11
by  :  Kris Huang

for : parse data from other platforms to the format of our platform
'''

# define data schema of our platform

from aiohttp import ClientSession
import json
import base64


class Base(object):

    def __init__(self, **kwargs):

        third = kwargs["third"]
        name = kwargs["name"]
        
        self.thirdparty = third
        
        if third:
            
            print("[ok] connect %s to third party server: %s" % (name, self.thirdparty))

        else:
            print("[ok] construct %s" % name)


    async def _asyncGetText(self, url, params):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            return await resp.text()


    async def _asyncGetJson(self, url, params):
        async with ClientSession() as session:
            resp = await session.get(url, params=params)
            return json.loads(await resp.text())


    async def _asyncPostJson(self, url, params):
        async with ClientSession() as session:
            resp = await session.post(url, data=params)
            return json.loads(await resp.text())


    async def _asyncGetJsonHeaders(self, url, params):
        async with ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                a = await resp.text()
                return json.loads(a)


    async def _asyncGetJsonHeadersCookies(self, url, params):
        async with ClientSession(cookies=self.cookies) as session:
            async with session.get(url, params=params, headers=self.headers) as resp:
                a = await resp.text()
                return json.loads(a)


    def _jsonify(self, _dict):

        return json.dumps(_dict).replace(" ", '')


    def _base64(self, text):
        
        return base64.b64decode(text).decode(encoding="utf-8-sig")



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

    def _song(self, p, res_id, com_id, mv_id, pic_url, alb_name, lrc_url, name, arts, time):
        return {
            "platform": p,
            "idforres": res_id,
            "idforcomments": com_id,
            "mvid": mv_id,
            "cover": pic_url,
            "albumname": alb_name,
            "lrcurl": lrc_url,
            "name": name,
            "artist": arts,
            "interval": time
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
        return {"uri": uri, "error": 1}

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
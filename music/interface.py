from .fetcher import Fetcher

class Music(Fetcher):

    def __init__(self, **kwargs):

        Fetcher.__init__(self, **kwargs)
        
        print("[ok] construct %s" % kwargs["name"])


    def _getname(self, singers):
        artist = ""
        for index, singer in enumerate(singers):
            if index == 0:
                artist += singer['name']
            else:
                artist += "," + singer['name']
        return artist


    def _song(self, p, res_id, com_id, mv_id, pic_url, alb_name, lrc_url, name, arts, time, playable=True):
        return {
            "platform": p,
            "idforres": res_id,
            "url":'/{}/song/{}'.format(self, p, res_id),
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


    def _songlist(self, p, id, name, pic, songnum):
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

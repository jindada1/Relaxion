try:
    from .baseparser import baseParser
except:
    from baseparser import baseParser


class KuGouparser(baseParser):
    def __init__(self, baseurl):
        self.baseurl = baseurl
        print("construct KuGou on %s" % baseurl)

    # override, return object
    async def searchSong(self, k, p, n):
        # this params is coincident with your creeper service
        params = {
            "keyword": k,
            "page": p,
            "pagesize": n,
            "plat": 2
        }
        # this api is coincident with your creeper service
        api = "https://mobilecdn.kugou.com/api/v3/search/song"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs': []}
        append = result['songs'].append
        try:
            for kugousong in jsonresp['data']['info']:
                append(self._song(
                    "kugou",
                    kugousong['hash'],
                    kugousong['hash'],
                    kugousong['mvhash'],
                    "/kugou/albumcover/%s" % kugousong['hash'],
                    kugousong["album_name"],
                    "/kugou/lyric/%s" %kugousong['songmid'],
                    kugousong['songname'],
                    kugousong['singername'],
                    kugousong['duration']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchAlbum(self, k, p, n):
        # this params is coincident with your creeper service
        params = {
            "searchkey": k,
            "page": p,
            "num": n
        }
        # this api is coincident with your creeper service
        api = "%s/search/album" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'albums': []}
        append = result['albums'].append
        try:
            for album in jsonresp['data']['album']['list']:
                append(self._album(
                    "kugou",
                    album['albumID'],
                    album['albumPic'],
                    album['albumName'],
                    album['albumID'],
                    self._getname(album['singer_list']),
                    album['publicTime']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchMV(self, k, p, n):
        # this params is coincident with your creeper service
        params = {
            "searchkey": k,
            "page": p,
            "num": n
        }
        # this api is coincident with your creeper service
        api = "%s/search/mv" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'videos': []}
        append = result['videos'].append
        try:
            for mv in jsonresp['data']['mv']['list']:
                append(self._mv(
                    "kugou",
                    mv['mv_name'],
                    mv['mv_pic_url'],
                    mv['v_id'],
                    mv['v_id'],
                    self._getname(mv['singer_list']),
                    mv['duration'],
                    mv['publish_date']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def mvuri(self, _id):
        # this params is coincident with your creeper service
        params = {
            "mvid": _id
        }
        # this api is coincident with your creeper service
        api = "%s/mv" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        return jsonresp

    # override
    async def musicuri(self, _id):
        # this params is coincident with your creeper service
        params = {
            "idforres": _id
        }
        # this api is coincident with your creeper service
        api = "%s/song" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        return jsonresp

    # override
    async def lyric(self, _id):
        # this params is coincident with your creeper service
        params = {
            "idforres": _id
        }
        # this api is coincident with your creeper service
        api = "%s/lyric" % self.baseurl
        textresp = await self._asyncGetText(api, params=params)
        return textresp

    # override
    async def songsinList(self, _id, p, n):
        # this params is coincident with your creeper service
        params = {
            "dissid": _id,
            "page": p,
            "num": n
        }
        # this api is coincident with your creeper service
        api = "%s/songs/songlist" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        
        result = {'songs':[]}
        append = result['songs'].append
        try:
            for kugousong in jsonresp['songlist']:
                append(self._song(
                    "kugou",
                    kugousong['songmid'],
                    kugousong['songid'],
                    kugousong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" + kugousong['albummid'] + ".jpg?max_age=2592000",
                    kugousong['albumname'],
                    "/kugou/lyric/" + kugousong['songmid'],
                    kugousong['songname'],
                    self._getname(kugousong['singer']),
                    kugousong['interval']
              ))
        except:
            result['error'] = 1
        return result

    # override
    async def songsinAlbum(self, _id):
        # this params is coincident with your creeper service
        params = {
            "albumid": _id
        }
        # this api is coincident with your creeper service
        api = "%s/songs/album" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs':[]}
        append = result['songs'].append
        try:
            for kugousong in jsonresp['data']['songlist']:
                append(self._song(
                    "kugou",
                    kugousong['songmid'],
                    kugousong['songid'],
                    kugousong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" + kugousong['albummid'] + ".jpg?max_age=2592000",
                    kugousong['albumname'],
                    "/kugou/lyric/" + kugousong['songmid'],
                    kugousong['songname'],
                    self._getname(kugousong['singer']),
                    kugousong['interval']
                ))
        except:
            result['error'] = 1
        return result

    # special
    async def getComments(self, _id, t, p, n):
        # this params is coincident with your creeper service
        params = {
            "idforcomments": _id,
            "type": t,
            "page": p,
            "num": n
        }
        # this api is coincident with your creeper service
        api = "%s/comments" % self.baseurl
        data = await self._asyncGetJson(api, params=params)
        # parse data
        result = {'hot': {'num': 0, 'comments': []},
                  'normal': {'num': 0, 'comments': []}}
        try:
            for comment in data['comment']['commentlist']:
                result['normal']['comments'].append(self._comment(
                    comment['avatarurl'],
                    comment['nick'],
                    comment['rootcommentcontent'],
                    comment['praisenum'],
                    comment['time']
                ))
        except:
            result['error'] = 1
            return result
        try:
            result['normal']['num'] = data['comment']['commenttotal']
            for comment in data['hot_comment']['commentlist']:
                result['hot']['comments'].append(self._comment(
                    comment['avatarurl'],
                    comment['nick'],
                    comment['rootcommentcontent'],
                    comment['praisenum'],
                    comment['time']
                ))
            result['hot']['num'] = data['hot_comment']['commenttotal']
        except:
            pass
        return result

    # special
    async def songinfo(self, songhash):
        # this params is coincident with your creeper service
        params = {
            "r": 'play/getdata',
            "hash": songhash
        }
        # this api is coincident with your creeper service
        api = "https://wwwapi.kugou.com/yy/index.php"
        data = await self._asyncGetJson(api, params=params)
    
    
    # special
    async def picurl(self, songhash):
        # first check db

        # search from KuGou

        pass

async def __test():
    p = QQparser("self-kugou")
    searchkey = "周杰伦"
    page = 2
    num = 20

    '''
        
    '''
    print((await p.searchSong(searchkey, page, num)).keys())
    # √ print((await p.searchAlbum(searchkey, page, num)).keys())
    # √ print((await p.searchMV(searchkey, page, num)).keys())
    # √ print((await p.getComments("107192078", "music", page, num)).keys())
    # √ print((await p.getComments("14536", "album", page, num)).keys())
    # √ print((await p.getComments("n0010BCw40a", "mv", page, num)).keys())
    # √ print((await p.musicuri("002WCV372JMZJw")).keys())
    # √ print((await p.mvuri("m00119xeo83")).keys())
    # √ print(await p.lyric("002WCV372JMZJw"))
    # √ print(await p.userlist("406143883"))
    # √ print((await p.songsinList("1304470181", page, num)).keys())
    # √ print((await p.songsinAlbum("14536")).keys())


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()

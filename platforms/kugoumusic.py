'''
on  :  2019-08-15
by  :  Kris Huang

for : get data from kugou music directly
'''

try:
    from .baseparser import baseParser
except:
    from baseparser import baseParser


class KuGouparser(baseParser):
    def __init__(self, baseurl):
        self.baseurl = baseurl
        print("construct KuGou on %s" % baseurl)

        self.cookies = {
            "kg_mid": 'af7c2445064307fc9ef998eff735b0d1',
            "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": '1565879171,1566012408,1566137661,1566286143',
            "kg_dfid": '10P9yI2EfXk70MCKMa4TFGjg'
        }

        self.headers={
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        '''
        {
            "{{hash}}":{{data}}
        }
        '''
        self.songinfoCache = {}

    # override, return object
    async def searchSong(self, k, p, n):
        # this params is coincident with kugou
        params = {
            "keyword": k,
            "page": p,
            "pagesize": n,
            "plat": 2
        }
        # this api is from kugou
        api = "http://mobilecdn.kugou.com/api/v3/search/song"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs': []}
        append = result['songs'].append
        try:
            for song in jsonresp['data']['info']:
                append(self._song(
                    "kugou",
                    song['hash'],
                    song['hash'],
                    song['mvhash'],
                    "/kugou/albumcover/%s" % song['hash'],
                    song["album_name"],
                    "/kugou/lyric/%s" % song['hash'],
                    song['songname'],
                    song['singername'],
                    song['duration']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchAlbum(self, k, p, n):
        # this params is coincident with kugou
        params = {
            "keyword": k,
            "page": p,
            "pagesize": n,
            "plat": 2
        }
        # this api is from kugou
        api = "http://mobilecdn.kugou.com/api/v3/search/album"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'albums': []}
        append = result['albums'].append
        try:
            for album in jsonresp['data']['info']:
                append(self._album(
                    "kugou",
                    album['albumid'],
                    album['imgurl'],
                    album['albumname'],
                    album['albumid'],
                    album['singername'],
                    album['publishtime']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchMV(self, k, p, n):
        # this params is coincident with kugou
        params = {
            "keyword": k,
            "page": p,
            "pagesize": n,
            "plat": 2
        }
        # this api is from kugou
        api = "http://mobilecdn.kugou.com/api/v3/search/mv"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'videos': []}
        append = result['videos'].append
        try:
            for mv in jsonresp['data']['info']:
                append(self._mv(
                    "kugou",
                    mv['filename'],
                    mv['imgurl'],
                    mv['hash'],
                    mv['hash'],
                    mv['singername'],
                    mv['duration'],
                    mv['publishdate']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def mvuri(self, _id):
        # this params is coincident with kugou
        params = {
            "mvid": _id
        }
        # this api is from kugou
        api = "%s/mv" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        return jsonresp

    # override
    async def musicuri(self, _hash):
        url = await self.dispatcher(_hash, "play_url")
        return self._uri(url)

    # override
    async def lyric(self, _hash):
        lrc = await self.dispatcher(_hash, "lyrics")
        return lrc

    # override
    async def songsinList(self, _id, p, n):
        # this params is coincident with kugou
        params = {
            "dissid": _id,
            "page": p,
            "num": n
        }
        # this api is from kugou
        api = "%s/songs/songlist" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)

        result = {'songs': []}
        append = result['songs'].append
        try:
            for song in jsonresp['songlist']:
                append(self._song(
                    "kugou",
                    song['songmid'],
                    song['songid'],
                    song['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    song['albummid'] + ".jpg?max_age=2592000",
                    song['albumname'],
                    "/kugou/lyric/" + song['songmid'],
                    song['songname'],
                    self._getname(song['singer']),
                    song['interval']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def songsinAlbum(self, _id):
        # this params is coincident with kugou
        params = {
            "albumid": _id
        }
        # this api is from kugou
        api = "%s/songs/album" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs': []}
        append = result['songs'].append
        try:
            for song in jsonresp['data']['songlist']:
                append(self._song(
                    "kugou",
                    song['songmid'],
                    song['songid'],
                    song['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    song['albummid'] + ".jpg?max_age=2592000",
                    song['albumname'],
                    "/kugou/lyric/" + song['songmid'],
                    song['songname'],
                    self._getname(song['singer']),
                    song['interval']
                ))
        except:
            result['error'] = 1
        return result

    # special
    async def getComments(self, _id, t, p, n):
        # this params is coincident with kugou
        params = {
            "idforcomments": _id,
            "type": t,
            "page": p,
            "num": n
        }
        # this api is from kugou
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
    async def dispatcher(self, _hash, key):
        print('key is %s' % key)
        if _hash in self.songinfoCache.keys():
            # hit
            print('hit: ' + key)
            while not self.songinfoCache[_hash]:
                # aready fetching, but no response, wait until data fetched or failed
                print('waiting')
                await asyncio.sleep(0.5)

            # directly fetch
            if self.songinfoCache[_hash]['data']:
                return self.songinfoCache[_hash]['data'][key]
        
        # not hit or overtime
        # add _hash to Cache, tell other requests to wait for response
        print('not hit: ' + key)
        self.songinfoCache[_hash] = {}

        # waiting
        data = await self.detail_info(_hash)

        # fill cache, for other requests to fetch 
        self.songinfoCache[_hash] = data

        if data['err_code'] == 0:
            return data['data'][key]
            
        return 'nores'

    # special
    async def detail_info(self, _hash):
        print('----------- getting -------------')
        # request from remote
        params = {
            "r": 'play/getdata',
            "hash": _hash
        }

        # this api is from kugou
        api = "https://wwwapi.kugou.com/yy/index.php"
        
        resp = await self.asyncGetJsonHeadersCookies(api, params=params)
        
        print(resp)

        return resp

    # special
    async def picurl(self, _hash):
        imgurl = await self.dispatcher(_hash, "img")
        return imgurl


async def __test():
    p = KuGouparser("local-creeper")
    searchkey = "周杰伦"
    page = 2
    num = 10
    songhash = "382DC60D2879205633FBB7F2685D9840"
    '''
        
    '''
    # √ print((await p.searchSong(searchkey, page, num)).keys())
    # √ print((await p.searchAlbum(searchkey, page, num)).keys())
    # √ print((await p.searchMV(searchkey, page, num)).keys())
    # await p.detail_info(songhash)

    await p.lyric(songhash)
    # print(await p.musicuri(songhash))
    # print(await p.picurl(songhash))

    # ? print((await p.getComments(songhash, "music", page, num)).keys())
    # ? print((await p.getComments("23509815", "album", page, num)).keys())
    # ? print((await p.getComments("0c28d3658d3ec86e9d033c80d9d8e9da", "mv", page, num)).keys())
    # ? print((await p.mvuri("0c28d3658d3ec86e9d033c80d9d8e9da")).keys())
    # ? print(await p.userlist("406143883"))
    # ? print((await p.songsinList("1304470181", page, num)).keys())
    # ? print((await p.songsinAlbum("23509815")).keys())
    

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()
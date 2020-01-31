'''
on  :  2019-08-15
by  :  Kris Huang

for : get data from kugou music directly
'''

try:
    from .baseparser import Music
except:
    from baseparser import Music


class KuGou(Music):
    def __init__(self, thirdparty = None):

        Music.__init__(self, name = "KuGou", third = thirdparty)
        
        self.cookies = {
            "kg_mid": 'af7c2445064307fc9ef998eff735b0d1',
            "Hm_lvt_aedee6983d4cfc62f509129360d6bb3d": '1565879171,1566012408,1566137661,1566286143',
            "kg_dfid": '10P9yI2EfXk70MCKMa4TFGjg'
        }

        self.headers = {
            'upgrade-insecure-requests': '1',  # important when '---/index.php' get play information
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

    # override, return object
    async def searchSong(self, k, p, n):
        # this params is coincident with kugou
        params = {
            "keyword": k,
            "page": int(p) + 1, # pages start from 1 in qq, we set to 0
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
                    "/gateway/kugou/albumcover/%s" % song['hash'],
                    song["album_name"],
                    "/gateway/kugou/lyric/%s" % song['hash'],
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
            "page": int(p) + 1, # pages start from 1 in qq, we set to 0
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
                    album['imgurl'].replace('{size}','150'),
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
        
        params = {
            "keyword": k,
            "page": int(p) + 1, # pages start from 1 in qq, we set to 0
            "pagesize": n,
            "plat": 2
        }
        
        api = "http://mobilecdn.kugou.com/api/v3/search/mv"
        jsonresp = await self._asyncGetJson(api, params=params)

        result = {'videos': []}
        append = result['videos'].append

        try:
            for mv in jsonresp['data']['info']:
                append(self._mv(
                    "kugou",
                    mv['filename'],
                    mv['imgurl'].replace('{size}','240'),
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
    async def mvuri(self, _hash):
        # this params is coincident with kugou
        params = {
            "hash": _hash,
            "cmd": 100,
            "ismp3": 1,
            "ext": 'mp4'
        }
        api = "http://m.kugou.com/app/i/mv.php"
        
        jsonresp = await self._asyncGetJson(api, params=params)
        try:
            url = list(jsonresp['mvdata'].items())[0][1]['downurl']
        except:
            url = None
        return self._uri(url)

    # override
    async def musicuri(self, _hash):

        params = {
            "r": 'play/getdata',
            "hash": _hash
        }
        
        api = "https://wwwapi.kugou.com/yy/index.php"

        result = await self._asyncGetJsonHeadersCookies(api, params=params)
        
        try:
            return self._uri(result['data']['play_url'])
        except:
            return self._uri()

    # override
    async def lyric(self, _hash):
        params = {                    
            'keyword':'%20-%20',
            'ver'    : '1',
            'hash'   : _hash,
            'client' : 'mobi',
            'man'    : 'yes',
        }
        
        api = 'http://krcs.kugou.com/search'

        data = await self._asyncGetJson(api, params=params)

        params = {
            'charset'  : 'utf8',
            'accesskey': data['candidates'][0]['accesskey'],
            'id'       : data['candidates'][0]['id'],
            'client'   : 'mobi',
            'fmt'      : 'lrc',
            'ver'      : '1',
        }

        api = 'http://lyrics.kugou.com/download'

        resp = await self._asyncGetJson(api, params=params)

        return self.base64decode(resp['content'])

    # override
    async def songsinList(self, _id, p, n):
        # n is 30
        params = {
            "specialid": _id,
            "page": p,
            'json': 'true'
        }
        
        api = "http://m.kugou.com/plist/list"
        jsonresp = await self._asyncGetJson(api, params=params)

        result = {'songs': []}
        append = result['songs'].append
        try:
            for song in jsonresp['list']['list']['info']:

                filname = song['filename'].split(' - ')

                append(self._song(
                    "kugou",
                    song['hash'],
                    song['hash'],
                    song['mvhash'],
                    "/gateway/kugou/albumcover/%s" % song['hash'],
                    song["remark"],
                    "/gateway/kugou/lyric/%s" % song['hash'],
                    filname[1],
                    filname[0],
                    song['duration']
                ))

        except:
            result['error'] = 1

        return result

    # override
    async def songsinAlbum(self, _id):
        # # this params is coincident with kugou
        # params = {
        #     "albumid": _id
        # }
        # # this api is from kugou
        # api = "%s/songs/album" % self.thirdparty
        # # jsonresp = await self._asyncGetJson(api, params=params)
        # songlist = []
        result = {'songs': []}
        # append = result['songs'].append
        # try:
        #     for song in songlist:
        #         append(self._song(
        #             "kugou",
        #             song['songmid'],
        #             song['songid'],
        #             song['vid'],
        #             "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
        #             song['albummid'] + ".jpg?max_age=2592000",
        #             song['albumname'],
        #             "/gateway/kugou/lyric/" + song['songmid'],
        #             song['songname'],
        #             self._getname(song['singer']),
        #             song['interval']
        #         ))
        # except:
        result['error'] = 1
        return result

    # special
    async def getComments(self, _id, t, p, n):
        
        # params = {
        #     "idforcomments": _id,
        #     "type": t,
        #     "page": p,
        #     "num": n
        # }
        
        # api = "%s/comments" % self.thirdparty
        # data = await self._asyncGetJson(api, params=params)
        # parse data
        result = {'hot': {'num': 0, 'comments': []},
                  'normal': {'num': 0, 'comments': []}}

        return result

    # special
    async def picurl(self, _hash):

        params = {
            "r": 'play/getdata',
            "hash": _hash
        }
        
        api = "https://wwwapi.kugou.com/yy/index.php"

        result = await self._asyncGetJsonHeadersCookies(api, params=params)

        return result['data']['img']


async def __test():

    p = KuGou()
    # searchkey = "周杰伦"
    # page = 2
    # num = 10
    songhash = "382DC60D2879205633FBB7F2685D9840"
    gbqq = "5FCE4CBCB96D6025033BCE2025FC3943"
    # mvhash = "1b43baaf79c20489c85def55e2ba7af0"
    '''
        test at 2019-09-26 14:06
    '''

    # √ print((await p.searchSong(searchkey, page, num)).keys())
    # √ print((await p.searchAlbum(searchkey, page, num)).keys())
    # √ print((await p.searchMV(searchkey, page, num)).keys())
    # √ print(await p.mvuri(mvhash))
    # √ print(await p.lyric(gbqq))
    print(await p.picurl(gbqq))
    # √ print((await p.songsinList("547134", page, num)).keys())

    # × print((await p.songsinAlbum("23509815")).keys())
    print(await p.musicuri(songhash))
    # × print((await p.getComments(songhash, "music", page, num)).keys())
    # × print((await p.getComments("23509815", "album", page, num)).keys())
    # × print((await p.getComments("0c28d3658d3ec86e9d033c80d9d8e9da", "mv", page, num)).keys())

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()
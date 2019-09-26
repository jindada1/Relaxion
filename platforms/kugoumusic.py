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
        self.headers = {
            'upgrade-insecure-requests': '1',  # important when '---/index.php' get play information
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

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
        
        params = {
            "keyword": k,
            "page": p,
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
        url = list(jsonresp['mvdata'].items())[0][1]['downurl']
        return self._uri(url)

    # override
    async def musicuri(self, _hash):
        params = {
            "hash": _hash,
            "key": 'play_url'
        }
        # this api is from local midware
        api = "%s/playres" % self.baseurl
        url = await self._asyncGetText(api, params=params)
        return self._uri(url)

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

        return self._base64(resp['content'])

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
                    "/kugou/albumcover/%s" % song['hash'],
                    song["remark"],
                    "/kugou/lyric/%s" % song['hash'],
                    filname[1],
                    filname[0],
                    song['duration']
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
    async def picurl(self, _hash):

        params = {
            "r": 'play/getdata',
            "hash": _hash
        }
        
        api = "https://wwwapi.kugou.com/yy/index.php"

        result = await self.asyncGetJsonHeadersCookies(api, params=params)

        img = result['data']['img']

        return self._uri(img)


async def __test():
    p = KuGouparser("http://localhost:8081/kugou")
    searchkey = "周杰伦"
    page = 2
    num = 10
    songhash = "382DC60D2879205633FBB7F2685D9840"
    gbqq = "5FCE4CBCB96D6025033BCE2025FC3943"
    '''
        
    '''
    # √ print((await p.searchSong(searchkey, page, num)).keys())
    # √ print((await p.searchAlbum(searchkey, page, num)).keys())
    # √ print((await p.searchMV(searchkey, page, num)).keys())
    # √ print(await p.mvuri("0c28d3658d3ec86e9d033c80d9d8e9da"))
    # √ print(await p.lyric(gbqq))
    # √ print(await p.picurl(gbqq))
    # √ print((await p.songsinList("547134", page, num)).keys())

    print((await p.songsinAlbum("23509815")).keys())

    # × print(await p.musicuri(songhash))
    # × print((await p.getComments(songhash, "music", page, num)).keys())
    # × print((await p.getComments("23509815", "album", page, num)).keys())
    # × print((await p.getComments("0c28d3658d3ec86e9d033c80d9d8e9da", "mv", page, num)).keys())

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()
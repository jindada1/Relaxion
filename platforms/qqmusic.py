'''
on  :  2019-07-11
by  :  Kris Huang

for : get data from qq music directly
'''

try:
    from .baseparser import baseParser
except:
    from baseparser import baseParser


class QQparser(baseParser):
    def __init__(self, baseurl):
        self.baseurl = baseurl

        self.headers = {
            'referer': 'http://y.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.cookies = {
            'p_luin': 'o2835893638',
            'p_lskey': '0004000024d53616cf3c76ca7ab957fa2c798af92411300d609c0c7f82168c0d0c60790e3e0ae9b2f1bd4eac',
        }

        self.commentMap = {
            'music':1,
            'song':1,
            'album':2,
            'mv':5
        }

        print("construct QQ on %s" % baseurl)

    # override, return object
    async def searchSong(self, k, p, n):
        # this params is coincident with your creeper service
        params = {
            # 'aggr':1, 聚合多版本音乐
            'remoteplace': 'txt.yqq.song',
            'format': 'json',
            't': 0,  # song
            'n': n,
            'p': p,
            'w': k
        }
        # this api is coincident with your creeper service
        api = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs': []}
        append = result['songs'].append
        try:
            for qqsong in jsonresp['data']['song']['list']:
                append(self._song(
                    "qq",
                    qqsong['songmid'],
                    qqsong['songid'],
                    qqsong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    qqsong['albummid'] + ".jpg?max_age=2592000",
                    qqsong['albumname'],
                    "/qq/lyric/" + qqsong['songmid'],
                    qqsong['songname'],
                    self._getname(qqsong['singer']),
                    qqsong['interval']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchAlbum(self, k, p, n):

        params = {
            'remoteplace': 'txt.yqq.album',
            't': 8,
            'format': 'json',
            'n': n,
            'p': p,
            'w': k
        }

        api = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'albums': []}
        append = result['albums'].append
        try:
            for album in jsonresp['data']['album']['list']:
                append(self._album(
                    "qq",
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

        params = {
            'remoteplace': 'txt.yqq.mv',
            't': 12,
            'format': 'json',
            'n': n,
            'p': p,
            'w': k
        }

        api = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'videos': []}
        append = result['videos'].append
        try:
            for mv in jsonresp['data']['mv']['list']:
                append(self._mv(
                    "qq",
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
    async def mvuri(self, mvid):

        params = {
            'data': self._jsonify({
                "getMvUrl": {
                    "module": "gosrf.Stream.MvUrlProxy",
                    "method": "GetMvUrls",
                    "param": {
                        "vids": [mvid],
                        "request_typet": 10001
                    }
                }
            })
        }

        api = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        jsonresp = await self.asyncGetJsonHeaders(api, params=params)

        mp4s = jsonresp['getMvUrl']['data'][mvid]['mp4']
        i = len(mp4s)
        while i > -1:
            i -= 1
            if len(mp4s[i]['freeflow_url']) > 0:
                return self._uri(mp4s[i]['freeflow_url'][0])

        hlses = jsonresp['getMvUrl']['data'][mvid]['hls']
        i = len(hlses)
        while i > -1:
            i -= 1
            if len(hlses[i]['freeflow_url']) > 0:
                return self._uri(hlses[i]['freeflow_url'][0])

        return self._uri("")

    # override
    async def musicuri(self, _id):
        # this params is coincident with your creeper service
        params = {
            "idforres": _id
        }
        # this api is coincident with your creeper service
        api = "%s/song" % self.baseurl
        jsonresp = await self._asyncGetJson(api, params=params)
        return self._uri(jsonresp['uri'])

    # override
    async def lyric(self, songmid):
        '''
        cache = CacheDB.getLyric(songmid)
        if cache:
            return cache
        '''

        params = {
            'format': 'json',
            'g_tk': 5381,
            'nobase64': 1,
            'songmid': songmid
        }

        api = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
        jsonresp = await self.asyncGetJsonHeaders(api, params=params)

        try:
            lyric = jsonresp['lyric']
            # CacheDB.addQQLyric(songmid, lyric)
        except:
            lyric = "没有歌词的纯音乐哦~"

        return lyric

    # override
    async def songsinList(self, _id, p, n):

        params = {
            'type': 1,
            'json': 1,
            'utf8': 1,
            'onlysong': 1,
            'nosign': 1,
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'notice': 0,
            'platform': 'yqq.json',
            'needNewCode': 0,
            'song_num': n,
            'song_begin': p*20,
            'disstid': _id
        }

        api = "https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg"
        jsonresp = await self.asyncGetJsonHeaders(api, params=params)

        result = {'songs': []}
        append = result['songs'].append
        try:
            for qqsong in jsonresp['songlist']:
                append(self._song(
                    "qq",
                    qqsong['songmid'],
                    qqsong['songid'],
                    qqsong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    qqsong['albummid'] + ".jpg?max_age=2592000",
                    qqsong['albumname'],
                    "/qq/lyric/" + qqsong['songmid'],
                    qqsong['songname'],
                    self._getname(qqsong['singer']),
                    qqsong['interval']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def songsinAlbum(self, _id):

        params = {
            'cmd': 'get_album_buy_page',
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'albumid': _id
        }

        api = "https://c.y.qq.com/v8/fcg-bin/musicmall.fcg"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs': []}
        append = result['songs'].append

        try:
            for qqsong in jsonresp['data']['songlist']:
                append(self._song(
                    "qq",
                    qqsong['songmid'],
                    qqsong['songid'],
                    qqsong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    qqsong['albummid'] + ".jpg?max_age=2592000",
                    qqsong['albumname'],
                    "/qq/lyric/" + qqsong['songmid'],
                    qqsong['songname'],
                    self._getname(qqsong['singer']),
                    qqsong['interval']
                ))
        except:
            result['error'] = 1
        return result

    # special
    async def getComments(self, _id, t, p, n):
        # this params is coincident with your creeper service
        params = {
            'cmd': 8,
            'format': 'json',
            'pagenum': p,
            'pagesize': n,
            'reqtype': 2,
            'biztype': self.commentMap[t],  # 1: for song ; 2: for album ; 5: for mv
            'topid': _id
        }

        api = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg"
        data = await self._asyncGetJson(api, params=params)
        print(data)
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
    async def userlist(self, qqnum):

        userid = CacheDB.getQQUserid(str(qqnum))

        if not userid:
            userid = await __getuserid(qqnum)
            CacheDB.addQQUserid(qqnum, userid)

        params = {
            "hostUin": 0,
            "format": "json",
            "cid": "205360838",
            "reqfrom": 1,
            "reqtype": 0,
            "userid": userid
        }

        api = "https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg"
        jsonresp = await self.asyncGetJsonHeadersCookies(api, params=params)

        data = jsonresp['data']
        res = {"allLists": [self._songlist(
            "qq",
            data['mymusic'][0]['id'],
            data['mymusic'][0]['title'],
            data['mymusic'][0]['laypic'],
            data['mymusic'][0]['num0']
        )]}
        for _list in data['mydiss']['list']:
            res["allLists"].append(self._songlist(
                "qq",
                _list['dissid'],
                _list['title'],
                _list['picurl'],
                int(_list['subtitle'].split('首')[0])
            ))
        return res

    # special
    async def __getuserid(qqnum):
        params = {
            'p': 1,
            'n': 30,
            'remoteplace': 'txt.yqq.user',
            'format': 'json',
            'searchid': '239684060216084795',
            'w': qqnum
        }

        api = "https://c.y.qq.com/soso/fcgi-bin/client_search_user"
        user = self.asyncGetJsonHeadersCookies['data']['user']['list'][0]
        result = {
            'title': user['title'],
            'pic': user['pic'],
            'userid': user['docid']
        }
        return user['docid']


async def __test():
    p = QQparser("http://api.goldenproud.cn/qq")
    searchkey = "周杰伦"
    page = 2
    num = 20

    '''
        test at 2019-09-25 20:11
    '''
    # √ print((await p.searchSong(searchkey, page, num)).keys())
    # √ print((await p.searchAlbum(searchkey, page, num)).keys())
    # √ print((await p.searchMV(searchkey, page, num)).keys())
    # - print((await p.getComments("107192078", "music", page, num)).keys())
    # - print((await p.getComments("14536", "album", page, num)).keys())
    # - print((await p.getComments("n0010BCw40a", "mv", page, num)).keys())
    # × print(await p.musicuri("002WCV372JMZJw"))
    # √ print(await p.mvuri("m00119xeo83"))
    # √ print(await p.lyric("002WCV372JMZJw"))
    # √ print(await p.userlist("406143883"))
    # √ print((await p.songsinList("1304470181", page, num)).keys())
    # √ print((await p.songsinAlbum("14536")).keys())


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()

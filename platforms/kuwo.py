'''
on  :  2019-07-11
by  :  Kris Huang

for : get data from qq music directly
'''

try:
    from .baseparser import Music
except:
    from baseparser import Music

import requests

class KuWo(Music):
    def __init__(self, thirdparty = None):

        Music.__init__(self, name = "KuWo", third = thirdparty)

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://kuwo.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Host': 'kuwo.cn',
        }

        self.get_cookie_token()
        
        self.cache = {}

        self.API_BASE = 'http://www.kuwo.cn/api/www'
        self.mv_pic_host = 'https://y.gtimg.cn/'


    def get_cookie_token(self):
        """get kuwo token & set cookie jar"""
        token_uri = 'http://kuwo.cn/search/list?key=hello'
        with requests.Session() as session:
            response = session.get(token_uri, headers=self.headers)
            token = response.cookies.get('kw_token')
            self.headers['csrf'] = token
            self.cookies = response.cookies

    def playable(self, number):
        '''
        song.switch 628481
        song.switch.toString(2) 10011001011100000001
        pop->reverse (19) ["0", "0", "0", "0", "0", "0", "0", "1", "1", "1", "0", "1", "0", "0", "1", "1", "0", "0", "1"]
        '''
        # convert decimal to binary code array
        string = list(bin(number))
        # remove last char
        string.pop()
        # reverse string
        string = string[::-1]
        play_flag = string[0]
        try_flag = string[13]
        return ((play_flag == '1') or ((play_flag == '1') and (try_flag == '1')))


    # override, return object
    async def searchSong(self, k, p, n):        
        # this params is coincident with kuwo
        params = {
            'rn': n,
            'pn': int(p) + 1, # pages start from 1 in kuwo, we set to 0
            'key': k
        }
        # this api is coincident with kuwo
        api = self.API_BASE + "/search/searchMusicBykeyWord"
        jsonresp = await self._asyncGetJsonHeadersCookies(api, params=params)
        
        result = {'songs': []}
        append = result['songs'].append
        try:
            for kuwosong in jsonresp['data']['list']:
                append(self._song(
                    "kuwo",
                    kuwosong['musicrid'],
                    kuwosong['rid'],
                    kuwosong['vid'],
                    kuwosong['albumpic'],
                    kuwosong['album'],
                    "/kuwo/lyric/" + kuwosong['rid'],
                    kuwosong['name'],
                    kuwosong['artist'],
                    kuwosong['duration'],
                    kuwosong['online']
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
            'p': int(p) + 1,
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
            'p': int(p) + 1,
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
            'data': self.jsonify({
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
        jsonresp = await self._asyncGetJsonHeaders(api, params=params)

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
        # this params is coincident with kuwo
        params = {
            'data': self.jsonify({
                "req_0":{
                    "module":"vkey.GetVkeyServer",
                    "method":"CgiGetVkey",
                    "param":{
                        "guid":"10000",
                        "songmid":[_id],
                        "songtype":[0],
                        "uin":"0",
                        "loginflag":1,
                        "platform":"20"
                    }
                }
            })
        }
        # this api is coincident with kuwo
        api = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        jsonresp = await self._asyncGetJson(api, params=params)
        
        try:
            info = jsonresp['req_0']['data']
            host = info['sip'][0]

            route = info['midurlinfo'][0]['purl']
            if route:
                return self._uri(host + route)

            return self._uri()

        except:
            return self._uri()

    # override
    async def lyric(self, songmid):
        params = {
            'format': 'json',
            'g_tk': 5381,
            'nobase64': 1,
            'songmid': songmid
        }

        api = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
        jsonresp = await self._asyncGetJsonHeaders(api, params=params)

        try:
            lyric = jsonresp['lyric']
        except:
            lyric = '[00:01.000] 没有歌词哦~'

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
            'song_begin': int(p)*int(n),   # page start from 0
            'disstid': _id
        }

        api = "https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg"
        jsonresp = await self._asyncGetJsonHeaders(api, params=params)

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
        # this params is coincident with kuwo
        params = {
            'cmd': 8,
            'format': 'json',
            'pagenum': p,  # start from 0
            'pagesize': n,
            'reqtype': 1,
            'biztype': self.commentMap[t],  # 1: for song ; 2: for album ; 5: for mv
            'topid': _id
        }

        api = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg"
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
                    self.to_time(comment['time'])
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
                    self.to_time(comment['time'])
                ))
            result['hot']['num'] = data['hot_comment']['commenttotal']
        except:
            pass
        return result

    # special
    async def userlist(self, qqnum):

        userid = await self.getuserid(qqnum)

        if userid:
            
            return await self.userdetail(userid)
        
        return ['no user matched']

    # special
    async def userdetail(self, userid):

        params = {
            "hostUin": 0,
            "format": "json",
            "cid": "205360838",
            "reqfrom": 1,
            "reqtype": 0,
            "userid": userid
        }

        api = "https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg"
        jsonresp = await self._asyncGetJsonHeadersCookies(api, params=params)
        
        try:
            data = jsonresp['data']
            res = {"lists": [self._songlist(
                "qq",
                data['mymusic'][0]['id'],
                data['mymusic'][0]['title'],
                data['mymusic'][0]['laypic'],
                data['mymusic'][0]['num0']
            )]}
            for _list in data['mydiss']['list']:
                res["lists"].append(self._songlist(
                    "qq",
                    _list['dissid'],
                    _list['title'],
                    _list['picurl'],
                    int(_list['subtitle'].split('首')[0])
                ))
            return res

        except:
            return []

    # special
    async def getuserid(self, qqnum):

        if qqnum in self.cache.keys():
            print('hit cache')
            return self.cache[qqnum]

        params = {
            'p': 1,
            'n': 30,
            'remoteplace': 'txt.yqq.user',
            'format': 'json',
            'searchid': '239684060216084795',
            'w': qqnum
        }

        api = "https://c.y.qq.com/soso/fcgi-bin/client_search_user"
        
        resp = await self._asyncGetJsonHeadersCookies(api, params)
        
        try:
            userid = resp['data']['user']['list'][0]['docid']
            self.cache[qqnum] = userid
            return userid

        except:
            return False


async def test():
    
    p = KuWo()
    searchkey = "周杰伦"
    page = 2
    num = 20
    userid = '7ensoKviNeci'

    # test at 2019-09-25 20:11
    
    print((await p.searchSong(searchkey, page, num)).keys())
    # √ print((await p.searchAlbum(searchkey, page, num)).keys())
    # √ print((await p.searchMV(searchkey, page, num)).keys())
    # √ print((await p.getComments("107192078", "music", page, num)).keys())
    # √ print((await p.getComments("14536", "album", page, num)).keys())
    # √ print((await p.getComments("n0010BCw40a", "mv", page, num)).keys())
    # - print(await p.musicuri("002WCV372JMZJw"))
    # √ print(await p.mvuri("m00119xeo83"))
    # √ print(await p.lyric("002WCV372JMZJw"))
    # √ print(await p.getuserid("406143883"))
    # print(await p.userlist("406143883"))
    # √ print(await p.userdetail(userid))
    # √ print((await p.songsinList("1304470181", page, num)).keys())
    # √ print((await p.songsinAlbum("14536")).keys())


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())

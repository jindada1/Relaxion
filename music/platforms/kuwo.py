'''
on  :  2019-07-11
by  :  Kris Huang

for : get data from kuwo music
'''
from music import Music

class KuWo(Music):

    def __init__(self):

        Music.__init__(self, name = "KuWo")

        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://kuwo.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'Host': 'kuwo.cn',
        }

        # self.get_cookie_token()
        
        self.cache = {}

        self.API_BASE = 'http://www.kuwo.cn/api/www'
        self.mv_pic_host = 'https://y.gtimg.cn/'

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
        # return jsonresp
        result = {'songs': []}
        append = result['songs'].append
        try:
            for kuwosong in jsonresp['data']['list']:
                append(self._song(
                    "kuwo",
                    kuwosong['musicrid'],
                    kuwosong['rid'],
                    kuwosong['rid'],
                    kuwosong['albumpic'],
                    kuwosong['album'],
                    "/kuwo/lyric/" + str(kuwosong['rid']),
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
            'rn': n,
            'pn': int(p) + 1, # pages start from 1 in kuwo, we set to 0
            'key': k
        }

        api = self.API_BASE + "/search/searchAlbumBykeyWord"
        jsonresp = await self._asyncGetJsonHeadersCookies(api, params=params)
        result = {'albums': []}
        append = result['albums'].append
        try:
            for album in jsonresp['data']['albumList']:
                append(self._album(
                    "kuwo",
                    album['albumid'],
                    album['pic'],
                    album['album'],
                    album['albumid'],
                    album['artist'],
                    album['releaseDate']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchMV(self, k, p, n):

        params = {
            'rn': n,
            'pn': int(p) + 1, # pages start from 1 in kuwo, we set to 0
            'key': k
        }

        api = "https://www.kuwo.cn/api/www/search/searchMvBykeyWord"
        jsonresp = await self._asyncGetJsonHeadersCookies(api, params=params)
        result = {'videos': []}
        append = result['videos'].append
        try:
            for mv in jsonresp['data']['mvlist']:
                append(self._mv(
                    "kuwo",
                    mv['name'],
                    mv['pic'],
                    mv['id'],
                    mv['id'],
                    mv['artist'],
                    mv['duration'],
                    '未知'
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def mvuri(self, mvid):

        params = {
            'rid': mvid,
            'response': 'url',
            'format': 'mp4|mkv',
            'type': 'convert_url',
            't': '1589586895402'
        }

        api = 'http://kuwo.cn/url'
        
        url = await self._asyncGetTextHeadersCookies(api, params=params)

        return self._uri(url)

    # override
    async def musicuri(self, _id):
        # this params is coincident with kuwo
        params = {
            'format': 'mp3',
            'rid': _id,
            'response': 'url',
            'type': 'convert_url3',
            'br': '128kmp3',
            'from': 'web',
            't': 1589364222048
        }
        # this api is coincident with kuwo
        api = 'http://kuwo.cn/url'
        jsonresp = await self._asyncGetJsonHeadersCookies(api, params=params)
        
        try:
            return self._uri(jsonresp['url'])

        except:
            return self._uri()

    def formatlyric(self, line):
        """
        line is {
            "time": "12.38",
            "lineLyric": "Wah wuh wu wa wa wua wua wua wa wa wua wu"
        }
        """
        t = line['time']
        minute = ('00' + str(int(float(t)) // 60))[-2:]
        second = ('00' + str(int(float(t)) % 60))[-2:]
        millsec = (t.split('.')[1] + "00")[:2]
        return f"[{minute}:{second}.{millsec}]" + line['lineLyric'] + "\n"

    # override
    async def lyric(self, songid):
        params = {
            'musicId': songid
        }

        api = "http://m.kuwo.cn/newh5/singles/songinfoandlrc"
        jsonresp = await self._asyncGetJsonHeadersCookies(api, params=params)
        
        lyric = ""

        try:
            for line in jsonresp['data']['lrclist']:
                lyric += self.formatlyric(line)

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

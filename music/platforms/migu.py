'''
on  :  2020-04-09
by  :  Kris Huang

for : get data from migu music
'''

from music import Music

class MiGu(Music):

    def __init__(self):

        Music.__init__(self, name="MiGu")

        self.headers = {
            'referer': 'http://music.migu.cn/',
            'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }

        self.cookies = {}

        self.commentMap = {
            'music': 1,
            'song': 1,
            'album': 2,
            'mv': 5
        }

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
        params = {
            'rows': n,
            'type': 2,
            'keyword': k,
            'pgc': p
        }

        api = "http://m.music.migu.cn/migu/remoting/scr_search_tag"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'songs': []}
        append = result['songs'].append
        try:
            for mgsong in jsonresp['musics']:
                append(self._song(
                    "migu",
                    "%s|%s" % (mgsong['copyrightId'], mgsong['id']),
                    mgsong['id'],
                    mgsong['mvCopyrightId'],
                    mgsong['cover'],
                    mgsong['albumName'],
                    "/migu/lyric/" + mgsong['copyrightId'],
                    mgsong['title'],
                    mgsong['singerName'],
                    -1,
                    True
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchAlbum(self, k, p, n):
        params = {
            'rows': n,
            'type': 4,
            'keyword': k,
            'pgc': p
        }

        api = "http://m.music.migu.cn/migu/remoting/scr_search_tag"
        jsonresp = await self._asyncGetJson(api, params=params)
        result = {'albums': []}
        append = result['albums'].append
        try:
            for album in jsonresp['albums']:
                append(self._album(
                    "migu",
                    album['id'],
                    album['albumPicM'],
                    album['title'],
                    album['id'],
                    self._getname(album['singer']),
                    album['publishDate']
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchMV(self, k, p, n):

        params = {
            "ua": "Android_migu",
            "version": "5.0.1",
            "text": k,
            "pageNo": p,
            "pageSize": n,
            "searchSwitch": '{"song":1,"album":0,"singer":0,"tagSong":0,"mvSong":0,"songlist":0,"bestShow":1}',
        }

        api = "http://pd.musicapp.migu.cn/MIGUM2.0/v1.0/content/search_all.do"
        jsonresp = await self._asyncGetJsonHeaders(api, params=params)
        return jsonresp

        result = {'videos': []}
        append = result['videos'].append
        try:
            for mv in jsonresp['mv']:
                append(self._mv(
                    "migu",
                    mv['title'],
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
    async def musicuri(self, cid_id):

        cid, _id = cid_id.split("|")
        params = {
            'id': _id,
            'cid': cid
        }
        # this api is coincident with your creeper service
        api = "http://api.migu.jsososo.com/song"
        jsonresp = await self._asyncGetJson(api, params=params)

        qualities = ['flac', '320k', '128k']
        try:
            data = jsonresp['data']
            for q in qualities:
                if q in data.keys():
                    return self._uri(data[q])

        except:
            pass
        return self._uri()

    # override
    async def lyric(self, songid):
        params = {
            'copyrightId': songid
        }

        api = "http://music.migu.cn/v3/api/music/audioPlayer/getLyric"
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
            for mgsong in jsonresp['songlist']:
                append(self._song(
                    "migu",
                    mgsong['songmid'],
                    mgsong['songid'],
                    mgsong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    mgsong['albummid'] + ".jpg?max_age=2592000",
                    mgsong['albumname'],
                    "/migu/lyric/" + mgsong['songmid'],
                    mgsong['songname'],
                    self._getname(mgsong['singer']),
                    mgsong['interval']
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
            for mgsong in jsonresp['data']['songlist']:
                append(self._song(
                    "migu",
                    mgsong['songmid'],
                    mgsong['songid'],
                    mgsong['vid'],
                    "https://y.gtimg.cn/music/photo_new/T002R300x300M000" +
                    mgsong['albummid'] + ".jpg?max_age=2592000",
                    mgsong['albumname'],
                    "/migu/lyric/" + mgsong['songmid'],
                    mgsong['songname'],
                    self._getname(mgsong['singer']),
                    mgsong['interval']
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
    async def userlist(self, user):

        return ['no user matched']

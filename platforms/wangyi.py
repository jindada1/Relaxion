try:
    from .baseparser import Music
except:
    from baseparser import Music

from Crypto.Cipher import AES
import binascii
import os



class WangYi(Music):
    def __init__(self, thirdparty = None):

        Music.__init__(self, name = "WangYi", third = thirdparty)

        self.headers = {
            'Referer'       : 'https://music.163.com',
            'Content-Type'  : 'application/x-www-form-urlencoded',
            'User-Agent'    : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }

        self.commentType = {
            'music'     : 'R_SO_4_',
            'mv'        : 'R_MV_5_',
            'album'     : 'R_AL_3_',
            'songlist'  : 'A_PL_0_',
            'radio'     : 'A_DJ_1_',
            'video'     : 'R_VI_62_',
            'dynamic'   : 'A_EV_2_'
        }

    def playable(self, fee):

        return not (fee == 4 or fee == 1);

    def encrypted_request(self, data) -> dict:
        MODULUS = (
            "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7"
            "b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280"
            "104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932"
            "575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b"
            "3ece0462db0a22b8e7"
        )
        PUBKEY = "010001"
        NONCE = b"0CoJUm6Qyw8W8jud"
        data = self.jsonify(data).encode("utf-8")
        secret = self.create_key(16)
        params = self.aes(self.aes(data, NONCE), secret)
        encseckey = self.rsa(secret, PUBKEY, MODULUS)
        
        return {"params": params.decode(), "encSecKey": encseckey}
        
    def aes(self, text, key):
        pad = 16 - len(text) % 16
        text = text + bytearray([pad] * pad)
        encryptor = AES.new(key, 2, b"0102030405060708")
        ciphertext = encryptor.encrypt(text)
        return self.base64encode(ciphertext)

    def rsa(self, text, pubkey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
        return format(rs, "x").zfill(256)

    def create_key(self, size):
        return binascii.hexlify(os.urandom(size))[:16]

    # override, return object
    async def searchSong(self, k, p, n):
        params = {
            'type': 1,
            'limit': n,
            'offset': int(p) * int(n),
            's': k
        }
        
        api = "http://music.163.com/api/search/pc"
        jsonresp = await self._asyncPostJson(api, params=params)

        result = {'songs': []}
        append = result['songs'].append
        try:
            for wangyisong in jsonresp['result']['songs']:
                append(self._song(
                    'wangyi',
                    wangyisong["id"],
                    wangyisong["id"],
                    wangyisong["mvid"],
                    "/gateway/wangyi/albumcover/%s" % wangyisong['album']['id'],
                    wangyisong["album"]['name'],
                    "/gateway/wangyi/lyric/%s" % wangyisong['id'],
                    wangyisong['name'],
                    self._getname(wangyisong['artists']),
                    int(wangyisong['duration']/1000),
                    self.playable(wangyisong['fee'])
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchAlbum(self, k, p, n):
        params = {
            's': k,
            'type': 10,  # 1: song, 10: album, 1004: MV 100: singer, 1000: songlist, 1002: user, 1006: 歌词, 1009: 电台, 1014: 视频
            'limit': n,
            'offset': int(p) * int(n),
        }

        api = "http://music.163.com/api/search/pc"
        jsonresp = await self._asyncPostJson(api, params=params)

        result = {'albums': []}
        append = result['albums'].append
        try:
            for album in jsonresp['result']['albums']:
                append(self._album(
                    'wangyi',
                    album['id'],
                    album['picUrl'],
                    album['name'],
                    album['id'],
                    self._getname(album['artists']),
                    album['publishTime'],
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchMV(self, k, p, n):
        params = {
            's': k,
            'type': 1004,  # 1: song, 10: album, 1004: MV 100: singer, 1000: songlist, 1002: user, 1006: 歌词, 1009: 电台, 1014: 视频
            'limit': n,
            'offset': int(p) * int(n),
        }

        api = "http://music.163.com/api/search/pc"
        jsonresp = await self._asyncPostJson(api, params=params)

        result = {'videos': []}
        append = result['videos'].append
        try:
            for mv in jsonresp['result']['mvs']:
                append(self._mv(
                    'wangyi',
                    mv['name'],
                    mv['cover'],
                    mv['id'],
                    mv['id'],
                    self._getname(mv['artists']),
                    int(mv['duration']/1000),
                    '-',
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def mvuri(self, _id):
        
        params = {
            "id": _id,
            "r": 1080
        }
        
        api = "https://music.163.com/weapi/song/enhance/play/mv/url"

        jsonresp = await self._asyncPostJson(api, params = self.encrypted_request(params))

        result = self._uri(jsonresp['data']['url'])

        return result

    # override
    async def musicuri(self, _id):

        params = self.encrypted_request(dict(ids=[_id], br=32000))

        api = "http://music.163.com/weapi/song/enhance/player/url"

        jsonresp = await self._asyncPostJson(api, params=params)

        result = self._uri(jsonresp['data'][0]['url'])

        return result

    # override
    async def lyric(self, _id):
        params = {
            "csrf_token": "",
            "id": _id,
            "lv": -1,
            "tv": -1
        }

        encrypt_data = self.encrypted_request(params)

        api = "https://music.163.com/weapi/song/lyric"
        jsonresp = await self._asyncPostJson(api, encrypt_data)

        lrc = '[00:01.000] 没有歌词哦~'

        try:
            lrc = jsonresp['lrc']['lyric']
        except:
            pass

        return lrc

    # override
    async def songsinList(self, _id, p, n):
        # no page, I made pages start from 0
        total = (int(p) + 1) * int(n)
        params = {
            "id" : _id,
            "limit" : total,
            "n" : total
        }
        
        api = "https://music.163.com/weapi/v3/playlist/detail"

        params = self.encrypted_request(params)

        jsonresp = await self._asyncPostJson(api, params = params)
        songscut = jsonresp['playlist']['tracks'][total-int(n):]

        result = {'songs':[]}
        append = result['songs'].append
        try:
            for wangyisong in songscut:
                append(self._song(
                    'wangyi',
                    wangyisong['id'],
                    wangyisong['id'],
                    wangyisong['mv'],
                    wangyisong['al']['picUrl'],
                    wangyisong['al']['name'],
                    "/gateway/wangyi/lyric/%s" % wangyisong['id'],
                    wangyisong['name'],
                    self._getname(wangyisong['ar']),
                    int(wangyisong['dt']/1000),
                    self.playable(wangyisong['fee'])
              ))
        except:
            result['error'] = 1
        return result

    # override
    async def songsinAlbum(self, _id):
        
        api = "https://music.163.com/weapi/v1/album/%s" % _id

        jsonresp = await self._asyncPostJson(api, params = self.encrypted_request({}))

        result = {'songs':[]}
        append = result['songs'].append
        try:
            for wangyisong in jsonresp['songs']:
                append(self._song(
                    'wangyi',
                    wangyisong['id'],
                    wangyisong['id'],
                    wangyisong['mv'],
                    wangyisong['al']['picUrl'],
                    wangyisong['al']['name'],
                    "/gateway/wangyi/lyric/%s" % wangyisong['id'],
                    wangyisong['name'],
                    self._getname(wangyisong['ar']),
                    "",
                    self.playable(wangyisong['fee'])
                ))
        except:
            result['error'] = 1
        return result

    # special
    async def getComments(self, _id, t, p, n):
        params = {
            "offset": int(p) * int(n),
            "limit": n,
            "rid": _id,
            "beforeTime": 0
        }

        api = "https://music.163.com/weapi/v1/resource/comments/%s" % (self.commentType[t] + _id)

        encrypt_data = self.encrypted_request(params)

        data = await self._asyncPostJson(api, params = encrypt_data)

        # parse data
        result = {'hot': {'num': 0, 'comments': []},
                  'normal': {'num': 0, 'comments': []}}
        try:
            for comment in data['comments']:
                result['normal']['comments'].append(self._comment(
                    comment['user']['avatarUrl'],
                    comment['user']['nickname'],
                    comment['content'],
                    comment['likedCount'],
                    self.to_time(int(comment['time']/1000))
                ))
            result['normal']['num'] = data['total']
        except:
            result['error'] = 1
            return result
        try:
            for comment in data['hotComments']:
                result['hot']['comments'].append(self._comment(
                    comment['user']['avatarUrl'],
                    comment['user']['nickname'],
                    comment['content'],
                    comment['likedCount'],
                    self.to_time(int(comment['time']/1000))
                ))
            result['hot']['num'] = len(data['hotComments'])
        except:
            pass
        return result

    # special
    async def userlist(self, user):
        
        searchparams = {
            "s":user,
            "type":1002
        }

        searchapi = "http://music.163.com/api/search/pc"
        userinfo = await self._asyncPostJson(searchapi, params=searchparams)

        uid = userinfo["result"]["userprofiles"][0]["userId"]

        # get user's playlist by uid
        params = {
            "uid": uid,
            "limit": 300,
            "offset": 0
        }
        
        api = "https://music.163.com/weapi/user/playlist"
        
        params = self.encrypted_request(params)

        jsonresp = await self._asyncPostJson(api, params = params)

        res = {"lists":[]}
        for _list in jsonresp['playlist']:
            res["lists"].append(self._songlist(
                "wangyi",
                _list['id'],
                _list['name'],
                _list['coverImgUrl'],
                _list['trackCount']
            ))
        return res

    # special
    async def picurl(self, _id):
        
        api = "https://music.163.com/weapi/v1/album/%s" % _id

        jsonresp = await self._asyncPostJson(api, params = self.encrypted_request({}))

        url = "https://i.loli.net/2020/01/31/9yvblCJoiVw1kAX.jpg"
        try:
            url = jsonresp['album']['picUrl']
        except:
            pass
        return url


async def __test():

    p = WangYi()
    searchkey = "林俊杰"
    page = 1
    num = 20
    '''
        test at 2020-01-25 21:27, all passed
    '''
    songs_0 = await p.searchSong(searchkey, 0, num)
    songs_1 = await p.searchSong(searchkey, 1, num)
    one = (songs_0['songs'][0]['idforres'] == songs_1['songs'][0]['idforres'])
    print('search: start from %s' % one)

    comments_0 = await p.getComments("33894312", "music", 0, num)
    comments_1 = await p.getComments("33894312", "music", 1, num)
    two = (comments_0['normal']['comments'][0]['username'] == comments_1['normal']['comments'][0]['username'])
    print('comments: start from %s' % two)

    list_0 = await p.songsinList("24381616", 0, num)
    list_1 = await p.songsinList("24381616", 1, num)
    three = (list_0['songs'][0]['idforres'] == list_1['songs'][0]['idforres'])
    print('list: start from %s' % three)

    # √ print((await p.searchSong(searchkey,page,num)).keys())
    # √ print((await p.searchAlbum(searchkey,page,num)).keys())
    # √ print((await p.searchMV(searchkey,page,num)).keys())
    # √ print((await p.getComments("33894312", "music", page, num)).keys())
    # √ print((await p.getComments("32311", "album", page, num)).keys())
    # √ print((await p.getComments("5436712", "mv", page, num)).keys())
    # √ print((await p.musicuri("33894312")).keys())
    # √ print((await p.mvuri("5436712")).keys())
    # √ print(len(await p.lyric("33894312")))
    # √ print(len(await p.lyric("33894312")))
    # √ print(await p.userlist("同济吴亦凡"))
    # √ print((await p.songsinList("24381616")).keys())
    # √ print((await p.songsinAlbum("32311")).keys())
    # √ print(await p.picurl("32311"))


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()

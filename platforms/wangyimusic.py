try:
    from .baseparser import baseParser
except:
    from baseparser import baseParser


class WangYiparser(baseParser):
    def __init__(self, thirdparty = None):

        baseParser.__init__(self, name = "WangYi", third = thirdparty)

    # override, return object
    async def searchSong(self, k, p, n):
        # this params is coincident with your creeper service
        params = {
            'keywords': k,
            'type': 1,  # 1: song, 10: album, 1004: MV 100: singer, 1000: songlist, 1002: user, 1006: 歌词, 1009: 电台, 1014: 视频
            'limit': n,
            'offset': int(p) * int(n),
        }
        # this api is coincident with your creeper service
        api = "%s/search" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)

        result = {'songs': []}
        append = result['songs'].append
        try:
            for wangyisong in jsonresp['result']['songs']:
                append(self._song(
                    'wangyi',
                    wangyisong["id"],
                    wangyisong["id"],
                    wangyisong["mvid"],
                    "/wangyi/albumcover/%s" % wangyisong['album']['id'],
                    wangyisong["album"]['name'],
                    "/wangyi/lyric/%s" % wangyisong['id'],
                    wangyisong['name'],
                    self._getname(wangyisong['artists']),
                    wangyisong['duration'],
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def searchAlbum(self, k, p, n):
        # this params is coincident with your creeper service
        params = {
            'keywords': k,
            'type': 10,  # 1: song, 10: album, 1004: MV 100: singer, 1000: songlist, 1002: user, 1006: 歌词, 1009: 电台, 1014: 视频
            'limit': n,
            'offset': int(p) * int(n),
        }
        # this api is coincident with your creeper service
        api = "%s/search" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)

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
        # this params is coincident with your creeper service
        params = {
            'keywords': k,
            'type': 1004,  # 1: song, 10: album, 1004: MV 100: singer, 1000: songlist, 1002: user, 1006: 歌词, 1009: 电台, 1014: 视频
            'limit': n,
            'offset': int(p) * int(n),
        }
        # this api is coincident with your creeper service
        api = "%s/search" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)

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
                    mv['duration'],
                    '-',
                ))
        except:
            result['error'] = 1
        return result

    # override
    async def mvuri(self, _id):
        # this params is coincident with your creeper service
        params = {
            "id": _id
        }
        # this api is coincident with your creeper service
        api = "%s/mv/url" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)
        result = self._uri(jsonresp['data']['url'])
        return result

    # override
    async def musicuri(self, _id):
        # this params is coincident with your creeper service
        params = {
            "id": _id
        }
        # this api is coincident with your creeper service
        api = "%s/song/url" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)
        result = self._uri(jsonresp['data'][0]['url'])
        return result

    # override
    async def lyric(self, _id):
        # this params is coincident with your creeper service
        params = {
            "id": _id
        }
        # this api is coincident with your creeper service
        api = "%s/lyric" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)

        return jsonresp['lrc']['lyric']

    # override
    async def songsinList(self, _id, p = 0, n = "all"):
        # this params is coincident with your creeper service
        params = {
            "id": _id
        }
        # this api is coincident with your creeper service
        api = "%s/playlist/detail" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)
        
        result = {'songs':[]}
        append = result['songs'].append
        try:
            for wangyisong in jsonresp['playlist']['tracks']:
                append(self._song(
                    'wangyi',
                    wangyisong['id'],
                    wangyisong['id'],
                    wangyisong['mv'],
                    wangyisong['al']['picUrl'],
                    wangyisong['al']['name'],
                    "/wangyi/lyric/%s" % wangyisong['id'],
                    wangyisong['name'],
                    self._getname(wangyisong['ar']),
                    wangyisong['dt'],
              ))
        except:
            result['error'] = 1
        return result

    # override
    async def songsinAlbum(self, _id):
        # this params is coincident with your creeper service
        params = {
            "id": _id
        }
        # this api is coincident with your creeper service
        api = "%s/album" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)
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
                    "/wangyi/lyric/%s" % wangyisong['id'],
                    wangyisong['name'],
                    self._getname(wangyisong['ar']),
                    "",
                ))
        except:
            result['error'] = 1
        return result

    # special
    async def getComments(self, _id, t, p, n):
        # this params is coincident with your creeper service
        params = {
            "offset": int(p) * int(n),
            "limit": n,
            "id": _id
        }
        # this api is coincident with your creeper service
        api = "%s/comment/%s" % (self.thirdparty, t)
        data = await self._asyncGetJson(api, params=params)
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
                    comment['time']
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
                    comment['time']
                ))
            result['hot']['num'] = len(data['hotComments'])
        except:
            pass
        return result

    # special
    async def userlist(self, user):
        # first search user, get user's id
        searchparams = {
            "keywords":user,
            "type":1002
        }
        searchapi = "%s/search" % self.thirdparty
        userinfo = await self._asyncGetJson(searchapi, params=searchparams)
        uid = userinfo["result"]["userprofiles"][0]["userId"]

        # get user's playlist by uid
        params = {
            "uid":uid
        }
        
        api = "%s/user/playlist" % self.thirdparty
        jsonresp = await self._asyncGetJson(api, params=params)
        res = {"allLists":[]}
        for _list in jsonresp['playlist']:
            res["allLists"].append(self._songlist(
                "wangyi",
                _list['id'],
                _list['name'],
                _list['coverImgUrl'],
                _list['trackCount']
            ))
        return res

    # special
    async def picurl(self, _id):
        params = {
            "id":_id
        }
        api = "%s/album" % self.thirdparty
        info = await self._asyncGetJson(api, params=params)
        return info['album']['picUrl'];


async def __test():
    p = WangYiparser("http://api.goldenproud.cn/wangyi")
    searchkey = "林俊杰"
    page = 1
    num = 20
    
    '''
        test at 2019-09-28 18:16, all passed
    '''
    # √ print((await p.searchSong(searchkey,page,num)).keys())
    # √ print((await p.searchAlbum(searchkey,page,num)).keys())
    # √ print((await p.searchMV(searchkey,page,num)).keys())
    # √ print((await p.getComments("33894312", "music", page, num)).keys())
    # √ print((await p.getComments("32311", "album", page, num)).keys())
    # √ print((await p.getComments("5436712", "mv", page, num)).keys())
    # √ print((await p.musicuri("33894312")).keys())
    # √ print((await p.mvuri("5436712")).keys())
    # √ print(await p.lyric("33894312"))
    # √ print(await p.userlist("同济吴亦凡"))
    # √ print((await p.songsinList("24381616")).keys())
    # √ print((await p.songsinAlbum("32311")).keys())
    
    # √ print(await p.picurl("32311"))


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__test())
    loop.close()

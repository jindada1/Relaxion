import re
import json
import time as Time
from aiohttp import ClientSession

async def getSearchSongs(searchkey,pageindex):
    params = {
        # 'aggr':1, 聚合多版本音乐
        'remoteplace':'txt.yqq.song',
        'format':'json',
        't':0, # song
        'n' : 20,
        'p' : pageindex,
        'w' : searchkey
    }

    return json.dumps(params)

async def getSearchMV(searchkey,pageindex):
    params = {
        'remoteplace':'txt.yqq.mv',
        't':12,
        'format':'json',
        'n' : 20,
        'p' : pageindex,
        'w' : searchkey
    }
    return json.dumps(params)

async def getSearchAlbum(searchkey,pageindex):
    params = {
        'remoteplace':'txt.yqq.album',
        't':8,
        'format':'json',
        'n' : 20,
        'p' : pageindex,
        'w' : searchkey
    }

    return json.dumps(params)

async def getAlbumSongs(albumid):
    params = {
        'cmd':'get_album_buy_page',
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'albumid':albumid
    }
    return json.dumps(params)

async def getSongsinList(disstid,pageindex = 0):
    params = {
        'type':1,
        'json':1,
        'utf8':1,
        'onlysong':1,
        'nosign':1,
        'format':'json',
        'inCharset':'utf8',
        'outCharset':'utf-8',
        'notice':0,
        'platform':'yqq.json',
        'needNewCode':0,
        'song_num':20,
        'song_begin':pageindex*20,
        'disstid':disstid
    }

    return json.dumps(params)

async def getComments(topid,biztype):
    params = {
        'cmd':8,
        'format':'json',
        'pagenum':0,
        'pagesize':25,
        'reqtype':2,
        'biztype':biztype, # 1: for song ; 2: for album ; 5: for mv
        'topid':topid
    }
    return json.dumps(params)

# test songmid: 002WCV372JMZJw 001J5QJL1pRQYB 003OUlho2HcRHC
async def getSonguri(songmid):
    params = {
        'vkey':key,
        'guid':'3757070001',
        'uid':0,
        'fromtag':30
    }

    return json.dumps(params)

async def getLyric(songmid):
    params = {
        'format':'json',
        'g_tk':5381,
        'nobase64':1,
        'songmid':songmid
    }
    return json.dumps(params)


# test mvid m00119xeo83 c0015vx9gdg
async def getMVuri(mvid):
    params = {
        'data':json.dumps({
            "getMvUrl":{
                "module":"gosrf.Stream.MvUrlProxy",
                "method":"GetMvUrls",
                "param":{
                    "vids":[mvid],
                    "request_typet":10001
                }
            }
        }).replace(" ",'')
    }
    return json.dumps(params)

async def getUserSonglists(qqnum):
    return qqnum


async def __main():
    print(getSongsinList('1304470181'))


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__main())
    loop.close()
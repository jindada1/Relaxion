import re
import json
import CacheDB
import time as Time
from reqConfig import *
from aiohttp import ClientSession

async def getSearchSongs(searchkey,pageindex):
    async with ClientSession() as session:
        params = {
            # 'aggr':1, 聚合多版本音乐
            'remoteplace':'txt.yqq.song',
            'format':'json',
            't':0, # song
            'n' : 20,
            'p' : pageindex,
            'w' : searchkey
        }
        async with session.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp',params=params) as resp:
            result = {'songs':[]}
            append = result['songs'].append
            try:
                for qqsong in json.loads(await resp.text())['data']['song']['list']:
                    append({
                        "platform": "qq",
                        "idforres": qqsong['songmid'],
                        "idforcomments": qqsong['songid'],
                        "mvid": qqsong['vid'],
                        "cover": "https://y.gtimg.cn/music/photo_new/T002R300x300M000" + qqsong['albummid'] + ".jpg?max_age=2592000",
                        "albumname": qqsong['albumname'],
                        "lrcurl": "/qq/lyric/" + qqsong['songmid'],
                        "name": qqsong['songname'],
                        "artist": __getname(qqsong['singer']),
                        "interval": qqsong['interval']
                    })
            except:
                result['error'] = "yes"
            return json.dumps(result)

async def getSearchMV(searchkey,pageindex):
    async with ClientSession() as session:
        params = {
            'remoteplace':'txt.yqq.mv',
            't':12,
            'format':'json',
            'n' : 20,
            'p' : pageindex,
            'w' : searchkey
        }
        async with session.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp',params=params) as resp:
            result = {'videos':[]}
            append = result['videos'].append
            try:
                for mv in json.loads(await resp.text())['data']['mv']['list']:
                    append({
                        "platform": "qq",
                        "name": mv['mv_name'],
                        "pic_url": mv['mv_pic_url'],
                        "mvid": mv['v_id'],
                        "idforcomments": mv['v_id'],
                        "artist": __getname(mv['singer_list']),
                        "duration": mv['duration'],
                        "publish_date": mv['publish_date']
                    })
            except:
                result['error'] = "yes"
            return json.dumps(result)

async def getSearchAlbum(searchkey,pageindex):
    async with ClientSession() as session:
        params = {
            'remoteplace':'txt.yqq.album',
            't':8,
            'format':'json',
            'n' : 20,
            'p' : pageindex,
            'w' : searchkey
        }
        async with session.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp',params=params) as resp:
            result = {'albums':[]}
            append = result['albums'].append
            try:
                for album in json.loads(await resp.text())['data']['album']['list']:
                    append({
                        "platform": "qq",
                        "albumid": album['albumID'],
                        "pic_url": album['albumPic'],
                        "name": album['albumName'],
                        "idforcomments": album['albumID'],
                        "artist": __getname(album['singer_list']),
                        "publish_date": album['publicTime']
                    })
            except:
                result['error'] = "yes"
            return json.dumps(result)

async def getAlbumSongs(albumid):
    async with ClientSession() as session:
        params = {
            'cmd':'get_album_buy_page',
            'format':'json',
            'inCharset':'utf8',
            'outCharset':'utf-8',
            'albumid':albumid
        }
        async with session.get('https://c.y.qq.com/v8/fcg-bin/musicmall.fcg',params=params) as resp:
            result = {'songs':[]}
            append = result['songs'].append
            try:
                for qqsong in json.loads(await resp.text())['data']['songlist']:
                    append({
                        "platform": "qq",
                        "idforres": qqsong['songmid'],
                        "idforcomments": qqsong['songid'],
                        "mvid": qqsong['vid'],
                        "cover": "https://y.gtimg.cn/music/photo_new/T002R300x300M000" + qqsong['albummid'] + ".jpg?max_age=2592000",
                        "albumname": qqsong['albumname'],
                        "lrcurl": "/qq/lyric/" + qqsong['songmid'],
                        "name": qqsong['songname'],
                        "artist": __getname(qqsong['singer']),
                        "interval": qqsong['interval']
                    })
            except:
                result['error'] = 1
            return json.dumps(result)

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
    async with ClientSession() as session:
        async with session.get('https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg', params=params, headers=header) as resp:
            result = {'songs':[]}
            append = result['songs'].append
            try:
                for qqsong in json.loads(await resp.text())['songlist']:
                    append({
                        "platform": "qq",
                        "idforres": qqsong['songmid'],
                        "idforcomments": qqsong['songid'],
                        "mvid": qqsong['vid'],
                        "cover": "https://y.gtimg.cn/music/photo_new/T002R300x300M000" + qqsong['albummid'] + ".jpg?max_age=2592000",
                        "albumname": qqsong['albumname'],
                        "lrcurl": "/qq/lyric/" + qqsong['songmid'],
                        "name": qqsong['songname'],
                        "artist": __getname(qqsong['singer']),
                        "interval": qqsong['interval']
                    })
            except:
                result['error'] = 1
            return json.dumps(result)

async def getComments(topid,biztype):
    async with ClientSession() as session:
        params = {
            'cmd':8,
            'format':'json',
            'pagenum':0,
            'pagesize':25,
            'reqtype':2,
            'biztype':biztype, # 1: for song ; 2: for album ; 5: for mv
            'topid':topid
        }
        async with session.get('https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg',params=params) as resp:
            data = json.loads(await resp.text())
            result = {'hot':{'num':0,'comments':[]},'normal':{'num':0,'comments':[]}}
            try:
                for comment in data['comment']['commentlist']:
                    result['normal']['comments'].append({
                        "avatar": comment['avatarurl'],
                        "username": comment['nick'],
                        "content": comment['rootcommentcontent'],
                        "stars": comment['praisenum'],
                        "time": comment['time']
                    })
                result['normal']['num'] = data['comment']['commenttotal']
                for comment in data['hot_comment']['commentlist']:
                    result['hot']['comments'].append({
                        "avatar": comment['avatarurl'],
                        "username": comment['nick'],
                        "content": comment['rootcommentcontent'],
                        "stars": comment['praisenum'],
                        "time": comment['time']
                    })
                result['hot']['num'] = data['hot_comment']['commenttotal']
            except:
                result['error'] = 1
            return json.dumps(result)

# test songmid: 002WCV372JMZJw 001J5QJL1pRQYB 003OUlho2HcRHC
async def getSonguri(songmid):
    try:
        key = await __getkey()
        cache = CacheDB.getMusicQuality(songmid)
        now = Time.time()
        if now - cache['time']  > 259200: # fresh quality every 3 days (3 * 24 * 60 * 60 sec)
            params = {
                'vkey':key,
                'guid':'3757070001',
                'uid':0,
                'fromtag':30
            }
            for index, quality in enumerate(qualities):
                async with ClientSession() as session:
                    testurl = "https://dl.stream.qqmusic.qq.com/" + quality[0] + songmid + quality[1]
                    async with session.get(testurl,params=params) as resp:
                        if resp.status == 200:
                            if cache['time'] == 0:
                                CacheDB.addMusicQuality(songmid,index,int(now))
                            else:
                                CacheDB.updateMusicQuality(songmid,index,int(now))
                            return json.dumps({'error':0,'uri':testurl})
            return json.dumps({'error':1,'uri':'no res'})
        else: # hit cache and do not exceed time limit
            print('get musicuri hit cache')
            uri = "https://dl.stream.qqmusic.qq.com/" + qualities[cache['quality']][0] + songmid + qualities[cache['quality']][1] + "?vkey=" + key + "&guid=3757070001&uid=0&fromtag=30";
            return json.dumps({'error':0,'uri':uri})
    except:
        return json.dumps({'error':1,'uri':'no key'})

async def getLyric(songmid):
    cache = CacheDB.getLyric(songmid)
    if cache:
        print('get lyric hit cache')
        return cache
    async with ClientSession() as session:
        params = {
            'format':'json',
            'g_tk':5381,
            'nobase64':1,
            'songmid':songmid
        }
        async with session.get('https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg',params=params,headers=header) as resp:
            try:
                lyric = json.loads(await resp.text())['lyric']
                CacheDB.addQQLyric(songmid,lyric)
            except:
                lyric = "没有歌词的纯音乐哦~"
            return lyric

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
    async with ClientSession() as session:
        async with session.get('https://u.y.qq.com/cgi-bin/musicu.fcg',params=params,headers=header) as resp:
            mp4s = json.loads(await resp.text())['getMvUrl']['data'][mvid]['mp4']
            i = len(mp4s)
            while i > -1:
                i -= 1
                if len(mp4s[i]['freeflow_url']) > 0:
                    return json.dumps({"error":0,"uri":mp4s[i]['freeflow_url'][0]})
            hlses = json.loads(await resp.text())['getMvUrl']['data'][mvid]['hls']
            i = len(hlses)
            while i > -1:
                i -= 1
                if len(hlses[i]['freeflow_url']) > 0:
                    return json.dumps({"error":0,"uri":hlses[i]['freeflow_url'][0]})
            return json.dumps({"error":1,"uri":""})

async def getUserSonglists(qqnum):
    userid = CacheDB.getQQUserid(str(qqnum))
    if not userid:
        userid = await __getuserid(qqnum)
        CacheDB.addQQUserid(qqnum,userid)
    return await __getSonglists(userid)

async def __getuserid(qqnum):
    params = {
        'p':1,
        'n':30,
        'remoteplace':'txt.yqq.user',
        'format':'json',
        'searchid':'239684060216084795',
        'w':qqnum
    }
    async with ClientSession(cookies=cookies) as session:
        async with session.get('https://c.y.qq.com/soso/fcgi-bin/client_search_user', headers=header, params=params) as resp:
            user = json.loads(await resp.text())['data']['user']['list'][0]
            result = {
                'title':user['title'],
                'pic':user['pic'],
                'userid':user['docid']
            }
            return user['docid']

async def __getSonglists(userid):
    params = {
        "hostUin":0,
        "format":"json",
        "cid":"205360838",
        "reqfrom":1,
        "reqtype":0,
        "userid":userid
    }
    async with ClientSession(cookies=cookies) as session:
        async with session.get('https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg', headers=header, params=params) as resp:
            data = json.loads(await resp.text())['data']
            res = {"allLists":[{
                "dissid": data['mymusic'][0]['id'],
                "name": data['mymusic'][0]['title'],
                "pic": data['mymusic'][0]['laypic'],
                "songnum": data['mymusic'][0]['num0'],
                "platform":"qq"
            }]}
            for _list in data['mydiss']['list']:
                res["allLists"].append({
                    "dissid": _list['dissid'],
                    "name": _list['title'],
                    "pic": _list['picurl'],
                    "songnum": re.findall(r"[1-9]\d*",_list['subtitle'])[0],
                    "platform":"qq"
                })
            return json.dumps(res)

def __getname(singers):
    artist = ""
    for index, singer in enumerate(singers):
        if index == 0:
            artist += singer['name']
        else:
            artist += "," + singer['name']
    return artist

cache = {
    'qqurikey' : {
        'value':'',
        'time':0
    }
}
async def __getkey():
    global cache
    t = int(Time.time())
    if t - cache['qqurikey']['time'] > 36000: # fresh key every 10 hours (10 * 60 * 60 sec)
        # get value key
        # guid is a random number % 10000000000 (10 chars)
        params = {
            'guid':'3757070001',
            'json':3,
            'format':'json'
        }
        async with ClientSession() as session:
            async with session.get('https://c.y.qq.com/base/fcgi-bin/fcg_musicexpress.fcg', headers=header, params = params) as resp:
                cache['qqurikey']['value'] = json.loads(await resp.text())['key']
                cache['qqurikey']['time'] = t
    return cache['qqurikey']['value']

async def __main():
    # print(await getLyric('002WCV372JMZJw'))
    # print(await getMVuri('m00119xeo83'))
    # print(await getAlbumSongs('1458791'))
    # print(await __getSonglists('7ensoKviNeci'))
    # await getUserSonglists('785136012')
    await getSongsinList('1304470181')
    pass


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__main())
    loop.close()
from aiohttp import web
import asyncQQ
import Parser from parser


async def index(request):
    return web.Response(\
        text='<div style="margin:auto">\
            <h2 style="color:green">Welcome To QQMusic Api !</h2>\
            <p>Demo list:</p>\
            <ul>\
                <li><a href="/search/song?searchkey=周杰伦&page=1">搜索“周杰伦”的歌曲的第 1 页</a></li>\
                <li><a href="/search/album?searchkey=周杰伦&page=2">搜索“周杰伦”的专辑的第 2 页</a></li>\
                <li><a href="/search/mv?searchkey=周杰伦&page=3">搜索“周杰伦”的MV的第 3 页</a></li>\
                <li><a href="/songs/album?albumid=1458791">获取专辑 id 为 1458791 里面的所有歌曲</a></li>\
                <li><a href="/songs/songlist?dissid=1304470181">获取歌单 id 为 1304470181 里面的歌曲</a></li>\
                <li><a href="/comments?idforcomments=14536&type=album">获取专辑 idforcomments 为 14536 的评论</a></li>\
                <li><a href="/comments?idforcomments=107192078&type=song">获取音乐 idforcomments 为 107192078 的评论</a></li>\
                <li><a href="/comments?idforcomments=n0010BCw40a&type=mv">获取mv idforcomments 为 n0010BCw40a 的评论</a></li>\
                <li><a href="/song?idforres=002WCV372JMZJw">获取音乐 idforres 为002WCV372JMZJw  的 uri</a></li>\
                <li><a href="/mv?mvid=m00119xeo83">获取mv id 为 m00119xeo83 的 uri</a></li>\
                <li><a href="/lyric?idforres=002WCV372JMZJw">获取音乐idforres 为 002WCV372JMZJw 的歌词内容</a></li>\
                <li><a href="/user/songlists?userid=10001">获取QQ号 为 10001 的 所有公开歌单</a></li>\
            </ul>\
            </div>',
        content_type='text/html')

# this function search songs from qq music, and format response then return out
async def searchSongs(request):
    try:
        searchkey = request.rel_url.query['searchkey']
    except:
        return web.Response(text="searchkey is required")
    try:
        pageindex = request.rel_url.query['page']
        if not pageindex:
            pageindex = 1
    except:
        pageindex = 1
    return web.Response(text = await asyncQQ.getSearchSongs(searchkey,pageindex))

async def searchMV(request):
    try:
        searchkey = request.rel_url.query['searchkey']
    except:
        return web.Response(text="searchkey is required")
    try:
        pageindex = request.rel_url.query['page']
        if not pageindex:
            pageindex = 1
    except:
        pageindex = 1
    return web.Response(text = await asyncQQ.getSearchMV(searchkey,pageindex))

async def searchAlbum(request):
    try:
        searchkey = request.rel_url.query['searchkey']
    except:
        return web.Response(text="searchkey is required")
    try:
        pageindex = request.rel_url.query['page']
        if not pageindex:
            pageindex = 1
    except:
        pageindex = 1
    return web.Response(text = await asyncQQ.getSearchAlbum(searchkey,pageindex))

# get songs in an album
async def songsinAlbum(request):
    try:
        albumid = request.rel_url.query['albumid']
    except:
        return web.Response(text="albumid is required")
    return web.Response(text=await asyncQQ.getAlbumSongs(albumid))

# get comments on a specific topic
async def commentsSong(request):
    try:
        topid = request.rel_url.query['idforcomments']
        biztype = commentMap[request.rel_url.query['type']]
        if not topid:
            return web.Response(text="idforcomments error")
    except:
        return web.Response(text="paraments error")
    return web.Response(text=await asyncQQ.getComments(topid,biztype))

async def commentsAlbum(request):
    try:
        topid = request.rel_url.query['idforcomments']
        biztype = commentMap[request.rel_url.query['type']]
        if not topid:
            return web.Response(text="idforcomments error")
    except:
        return web.Response(text="paraments error")
    return web.Response(text=await asyncQQ.getComments(topid,biztype))

async def commentsMV(request):
    try:
        topid = request.rel_url.query['idforcomments']
        biztype = commentMap[request.rel_url.query['type']]
        if not topid:
            return web.Response(text="idforcomments error")
    except:
        return web.Response(text="paraments error")
    return web.Response(text=await asyncQQ.getComments(topid,biztype))

# get the uri of a song 
async def songUri(request):
    try:
        idforres = request.rel_url.query['idforres']
        if not idforres:
            return web.Response(text="paraments error")
    except:
        return web.Response(text="paraments error")
    return web.Response(text = await asyncQQ.getSonguri(idforres))

# get lyric of a song
async def lyric(request):
    try:
        songmid = request.rel_url.query['idforres']
        if not songmid:
            return web.Response(text="paraments error")
    except:
        return web.Response(text="paraments error")
    return web.Response(text = await asyncQQ.getLyric(songmid))

# get the uri of a mv 
async def mvUri(request):
    try:
        vid = request.rel_url.query['mvid']
        if not vid:
            return web.Response(text="paraments error")
    except:
        return web.Response(text="paraments error")
    return web.Response(text = await asyncQQ.getMVuri(vid))

# get user's public songlists
async def userSonglists(request):
    try:
        userid = request.rel_url.query['userid']
        if not userid:
            return web.Response(text="userid error")
    except:
        return web.Response(text="userid error")
    return web.Response(text = await asyncQQ.getUserSonglists(userid))

# get songs in a user songlist
async def songsinSonglist(request):
    try:
        dissid = request.rel_url.query['dissid']
        if not dissid:
            return web.Response(text="dissid error")
    except:
        return web.Response(text="dissid error")
    try:
        pageindex = request.rel_url.query['page']
        if not pageindex:
            pageindex = 1
    except:
        pageindex = 1
    return web.Response(text = await asyncQQ.getSongsinList(dissid))

async def testDynamic(request):
    platform = request.match_info['platform']
    P = Parser.get(platform)
    if P:
        return web.json_response(P.testDynamic(request.path_qs))
    else:
        return web.Response(text="platform: %s is not supported" % platform)

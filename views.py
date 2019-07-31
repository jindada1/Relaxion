'''
on  :  2019-07-11
by  :  Kris Huang

for : check request params
      restrict request params (arrording to xxx_args, argSchema)
      dispatch request to services
'''

import re
from aiohttp import web
from platforms import PraserService
from db import dbService


othercfg = {}
superParser = PraserService(othercfg)
localdb = dbService('./db/User.db')


class argsCheckerGet(object):
    def __init__(self, argSchema):
        self.argSchema = argSchema

    def __call__(self, handler):
        def wrapper(request):
            # print("%s is running" % handler.__name__)
            req = request.path_qs
            print(req)

            # validate arguments in request according to self.argSchema
            validation = self.validate(request.rel_url)
            if validation['err']:
                return errorHandler(validation['err'])
            else:
                return handler(validation)
        return wrapper

    def validate(self, rq_args):
        params = {}
        for arg, prpty in self.argSchema.items():
            try:
                params[arg] = rq_args.query[arg]
            except:
                # if param is required, raise error
                if prpty == "*":
                    return {"err": "%s is required" % arg}
                # set default value
                params[arg] = prpty
        params["err"] = ""
        return params


class pltfGet(argsCheckerGet):
    def __init__(self, argSchema):

        super().__init__(argSchema)

    def __call__(self, handler):
        def wrapper(request):
            # print("%s is running" % handler.__name__)
            platform = request.match_info['platform']
            req = request.path_qs
            print(req)

            # filter invalid platforms
            if superParser[platform]:
                # validate arguments in request according to self.argSchema
                validation = self.validate(request.rel_url)
                if validation['err']:
                    return errorHandler(validation['err'])
                else:
                    return handler(superParser[platform], validation)
            # handle error platforms
            return errorHandler("platform: %s is not supported" % platform)
        return wrapper


async def errorHandler(errmsg):
    return web.Response(text=errmsg)


async def index(request):
    return web.FileResponse('./templates/index.html')


async def files(request):
    filename = request.match_info['filename']
    return web.FileResponse('./static/' + filename)

search_args = {
    "keyword": "*",
    "num": 20,
    "page": 0
}
# this function search songs from qq music, and format response then return out
# @pltfGet(search_args)


@pltfGet(search_args)
async def searchSong(P, params):
    s = params['keyword']
    p = params['page']
    n = params['num']
    return web.json_response(await P.searchSong(s, p, n))


@pltfGet(search_args)
async def searchMV(P, params):
    s = params['keyword']
    p = params['page']
    n = params['num']
    return web.json_response(await P.searchMV(s, p, n))


@pltfGet(search_args)
async def searchAlbum(P, params):
    s = params['keyword']
    p = params['page']
    n = params['num']
    return web.json_response(await P.searchAlbum(s, p, n))

# get songs in an album


@pltfGet({'albumid': "*"})
async def songsinAlbum(P, params):
    albumid = params['albumid']
    return web.json_response(await P.songsinAlbum(albumid))

# get comments on a specific topic
comment_args = {
    'idforcomments': "*",
    "num": 20,
    "page": 0
}


@pltfGet(comment_args)
async def commentsSong(P, params):
    topid = params['idforcomments']
    p = params['page']
    n = params['num']
    return web.json_response(await P.getComments(topid, 'music', p, n))


@pltfGet(comment_args)
async def commentsAlbum(P, params):
    topid = params['idforcomments']
    p = params['page']
    n = params['num']
    return web.json_response(await P.getComments(topid, 'album', p, n))


@pltfGet(comment_args)
async def commentsMV(P, params):
    topid = params['idforcomments']
    p = params['page']
    n = params['num']
    return web.json_response(await P.getComments(topid, 'mv', p, n))

# get the uri of a song


@pltfGet({'idforres': "*"})
async def songUri(P, params):
    idforres = params['idforres']
    return web.json_response(await P.musicuri(idforres))

# get the uri of a mv


@pltfGet({'mvid': "*"})
async def mvUri(P, params):
    mvid = params['mvid']
    return web.json_response(await P.mvuri(mvid))

# get user's public songlists


@pltfGet({'user': "*"})
async def userSonglists(P, params):
    user = params['user']
    return web.json_response(await P.userlist(user))

# get songs in a user songlist


@pltfGet({
    'dissid': "*",
    "num": 20,
    "page": 0
})
async def songsinSonglist(P, params):
    dissid = params['dissid']
    p = params['page']
    n = params['num']
    return web.json_response(await P.songsinList(dissid, p, n))

# get lyric of a song


def Redrict(handler):
    def wrapper(request):
        # print("%s is running" % handler.__name__)
        platform = request.match_info['platform']
        _id = request.match_info['id']
        print(request.path_qs)

        # filter invalid platforms
        if superParser[platform]:
            return handler(superParser[platform], _id)
        # handle error platforms
        return errorHandler("platform: %s is not supported" % platform)
    return wrapper


@Redrict
async def lyric(P, _id):
    return web.Response(text=await P.lyric(_id))


@Redrict
async def albumPic(P, _id):
    newurl = await P.picurl(_id)
    raise web.HTTPFound(newurl)


@Redrict
async def song(P, _id):
    newurl = await P.musicuri(_id)
    # newurl is {"uri":"https://......."}
    raise web.HTTPFound(newurl['uri'])


test_args = {
    "a": "*",
    "b": "1"
}


@pltfGet(test_args)
async def testDynamic(P, params):
    a = params['a']
    b = params['b']
    return web.json_response(P.testDynamic(a, b))


@argsCheckerGet({
    'username': "*"
})
async def getUserLove(params):
    userid = params['username']
    return web.json_response(localdb.get_songlist(userid))


class argsCheckerPost(object):
    def __init__(self, argSchema):
        self.argSchema = argSchema

    def __call__(self, handler):
        async def wrapper(request):
            # print("%s is running" % handler.__name__)
            req = request.path_qs
            print(req)

            # get form data
            data = await request.json()

            # validate arguments in request according to self.argSchema
            validation = self.validate(data)
            if validation['err']:
                return await errorHandler(validation['err'])
            else:
                return await handler(validation)
        return wrapper

    def validate(self, data):
        params = {}
        for arg, prpty in self.argSchema.items():
            # get value
            if arg in data.keys():
                params[arg] = data[arg]

            else:
                # if param is required, raise error
                if prpty == "*":
                    return {"err": "%s is required" % arg}
                # set default value
                params[arg] = prpty

        params["err"] = ""
        return params

@argsCheckerPost({
    'username': '*',
    'password': '*'
})
async def login(params):
    result = localdb.login({
        'name': params['username'],
        'pw': params['password']
    })
    return web.json_response(result)


@argsCheckerPost({
    'username': '*',
    'password': '*'
})
async def signUp(params):
    result = localdb.register({
        'name': params['username'],
        'pw': params['password']
    })
    return web.json_response(result)


async def loveSong(request):
    pass


async def hateSong(request):
    pass

from .baseview import BaseView, pltf_get, redrict


class Platforms(BaseView):

    def __init__(self, workers):

        self.parser = workers[0]

    search_args = {
        "keyword": "*",
        "num": 20,
        "page": 0
    }

    @pltf_get(search_args)
    async def searchSong(self, P, params):
        s = params['keyword']
        p = params['page']
        n = params['num']
        return self._json_response(await P.searchSong(s, p, n))

    @pltf_get(search_args)
    async def searchMV(self, P, params):
        s = params['keyword']
        p = params['page']
        n = params['num']
        return self._json_response(await P.searchMV(s, p, n))

    @pltf_get(search_args)
    async def searchAlbum(self, P, params):
        s = params['keyword']
        p = params['page']
        n = params['num']
        return self._json_response(await P.searchAlbum(s, p, n))

    @pltf_get({'albumid': "*"})
    async def songsinAlbum(self, P, params):
        albumid = params['albumid']
        return self._json_response(await P.songsinAlbum(albumid))

    # get comments on a specific topic
    comment_args = {
        'idforcomments': "*",
        "num": 20,
        "page": 0
    }

    @pltf_get(comment_args)
    async def commentsSong(self, P, params):
        topid = params['idforcomments']
        p = params['page']
        n = params['num']
        return self._json_response(await P.getComments(topid, 'music', p, n))

    @pltf_get(comment_args)
    async def commentsAlbum(self, P, params):
        topid = params['idforcomments']
        p = params['page']
        n = params['num']
        return self._json_response(await P.getComments(topid, 'album', p, n))

    @pltf_get(comment_args)
    async def commentsMV(self, P, params):
        topid = params['idforcomments']
        p = params['page']
        n = params['num']
        return self._json_response(await P.getComments(topid, 'mv', p, n))

    # get the uri of a song

    @pltf_get({'idforres': "*"})
    async def songUri(self, P, params):
        idforres = params['idforres']
        return self._json_response(await P.musicuri(idforres))

    # get the uri of a mv

    @pltf_get({'mvid': "*"})
    async def mvUri(self, P, params):
        mvid = params['mvid']
        return self._json_response(await P.mvuri(mvid))

    # get user's public songlists

    @pltf_get({'user': "*"})
    async def userSonglists(self, P, params):
        user = params['user']
        return self._json_response(await P.userlist(user))

    # get songs in a user songlist

    @pltf_get({
        'dissid': "*",
        "num": 20,
        "page": 0
    })
    async def songsinSonglist(self, P, params):
        dissid = params['dissid']
        p = params['page']
        n = params['num']
        return self._json_response(await P.songsinList(dissid, p, n))

    @pltf_get({'id': "*"})
    async def videoUri(self, P, params):
        _id = params['id']
        return self._json_response(await P.videouri(_id))

    # get lyric of a song

    @redrict
    async def lyric(self, P, _id):
        return self._textmsg(await P.lyric(_id))

    @redrict
    async def albumPic(self, P, _id):
        newurl = await P.picurl(_id)
        raise self._redrict_to(newurl)

    @redrict
    async def song(self, P, _id):
        newurl = await P.musicuri(_id)
        # newurl is {"uri":"https://......."}
        raise self._redrict_to(newurl['uri'])

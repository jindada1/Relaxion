from .baseview import BaseView, pltf_get, redirect
from music import PraserService


class Platforms(BaseView):

    def __init__(self, config):

        BaseView.__init__(self)
        self.parser = PraserService(config['platforms'])

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

    @redirect('txt')
    async def lyric(self, P, _id):
        return await P.lyric(_id)

    @redirect('url')
    async def albumPic(self, P, _id):
        return await P.picurl(_id)

    @redirect('url')
    async def song(self, P, _id):
        result = await P.musicuri(_id)
        # result is {"uri":"https://......."}
        return result['uri']

    @redirect('url')
    async def redirect(self, P, _id):
        url = P.mvpicCDN(_id)
        return url[:-1]

    

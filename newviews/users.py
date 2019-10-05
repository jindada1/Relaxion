from .baseview import BaseView, check_args_post, check_args_get

class Users(BaseView):
    '''
    this class contains many functions for user db
    '''
    def __init__(self, workers):
        
        self.localdb = workers[0]


    @check_args_get({
        'username': "*"
    })
    async def getUserLove(self, params):
        userid = params['username']
        return self._json_response(self.localdb.get_songlist(userid))


    @check_args_post({
        'username': '*',
        'password': '*'
    })
    async def login(self, params):
        result = self.localdb.login({
            'name': params['username'],
            'pw': params['password']
        })
        return self._json_response(result)


    @check_args_post({
        'username': '*',
        'password': '*'
    })
    async def signUp(self, params):
        result = self.localdb.register({
            'name': params['username'],
            'pw': params['password']
        })
        return self._json_response(result)


    @check_args_post({
        'username': '*',
        'songid': '*',
        'info_str': '*'
    })
    async def loveSong(self, params):
        result = self.localdb.love_song(
            params['username'],
            params['songid'],
            params['info_str']
        )
        return self._json_response(result)


    @check_args_post({
        'username': '*',
        'songid': '*'
    })
    async def hateSong(self, params):
        result = self.localdb.hate_song(
            params['username'],
            params['songid']
        )
        return self._json_response(result)

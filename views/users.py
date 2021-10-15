from .baseview import BaseView, check_args_post, check_args_get, check_args_upload
from db import dbService

class Users(BaseView):
    '''
    this class contains many functions for user db
    '''
    def __init__(self, config):
        
        self.localdb = dbService(config['database'])


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
        'name': '*',
        'pw': '*',
        'info':'*'
    })
    async def update(self, params):
        result = self.localdb.update({
            'name': params['name'],
            'pw': params['pw'],
            'info': params['info']
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


    @check_args_upload({
        'user': "*"
    })
    async def uploadAvator(self, meta):
        
        b_file = meta['file']
        user = meta['user']

        avator_path = './resource/avators/%s.jpg'% user

        try:
            with open(avator_path, 'wb') as f:

                f.write(b_file)

            self.localdb.update_avator(user, avator_path)

            return self._json_response({"url": url})

        except:
            return self._json_response({"err": "failed"})
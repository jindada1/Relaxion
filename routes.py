'''
setup routes
'''
from views import *


class RouteService(object):
    """
    路由类
    """
    def __init__(self, method, path, handler):
        self.method = method
        self.path = path
        self.handler = handler


def setup_routes(app, config: dict):

    static_resources(app, config)

    setup_services(app, user_service(config), '/user')

    setup_services(app, music_platforms(config), '/music')

    setup_services(app, core_functions(config), '/core')


def setup_services(app, services, prefix=None):

    if not prefix:
        assert prefix.startswith('/')
        assert not prefix.endswith('/')
        assert len(prefix) > 1

    for service in services:
        path = prefix + service.path
        app.router.add_route(service.method, path, service.handler)


def static_resources(app, config: dict, prefix=''):
    '''
    static resources
    '''
    # app.router.add_static('/kris/', path='front/admin/', name='admin', show_index=True)

    app.router.add_static('/resource/', path='core/resources', name='resource', show_index=True)


def core_functions(config: dict):
    '''
    core functions
    '''
    core = Cores(config)

    return [
        # extract music from mv
        RouteService('post', '/extract', core.extractAudio),

        # start download
        RouteService('post', '/download', core.downloadRes),

        # get download progress
        RouteService('get', '/download/progress', core.dlProgress),
    ]


def user_service(config: dict):
    '''
    user service
    '''
    user = Users(config)
    return [
        # user login
        RouteService('post', '/login', user.login),

        # user sign up
        RouteService('post', '/sign', user.signUp),

        # user love a song, add song to his list
        RouteService('post', '/love/song', user.loveSong),

        # get user loved songs
        RouteService('get', '/loved/songs', user.getUserLove),

        # user dislike a song, remove song from his list
        RouteService('post', '/hate/song', user.hateSong),

        # update user's info
        RouteService('post', '/info/update', user.update),

        # upload avator
        RouteService('post', '/upload/avator', user.uploadAvator),
    ]


def music_platforms(config: dict):
    '''
    controllers for music platforms' services
    '''
    platforms = Platforms(config)

    return [
        # search and return song
        RouteService('get', '/{platform}/songs', platforms.searchSong),

        # search and return album
        RouteService('get', '/{platform}/albums', platforms.searchAlbum),

        # search and return mv
        RouteService('get', '/{platform}/mv', platforms.searchMV),

        # get songs in an album
        RouteService('get', '/{platform}/songs/album', platforms.songsinAlbum),

        # get songs in a user songlist
        RouteService('get', '/{platform}/songs/songlist', platforms.songsinSonglist),

        # get comments of a song
        RouteService('get', '/{platform}/comments/song', platforms.commentsSong),

        # get comments of a album
        RouteService('get', '/{platform}/comments/album', platforms.commentsAlbum),

        # get comments of a mv
        RouteService('get', '/{platform}/comments/mv', platforms.commentsMV),

        # get lyric of a song
        RouteService('get', '/{platform}/lyric/{id}', platforms.lyric),

        # redirect to an effective uri of a song
        RouteService('get', '/{platform}/song/{id}', platforms.song),

        # get uri of a song
        RouteService('get', '/{platform}/uri/song', platforms.songUri),

        # get uri of a mv
        RouteService('get', '/{platform}/uri/mv', platforms.mvUri),

        # get user's public songlists
        RouteService('get', '/{platform}/user/songlists', platforms.userSonglists),

        # redirect pic
        RouteService('get', '/{platform}/albumcover/{id}', platforms.albumPic),

        # redirect
        RouteService('get', '/redirect/{platform}/{id:.+}', platforms.redirect),
    ]

'''
setup routes
'''
from views import *
from settings import url


def setup_routes(app, config: dict):

    static_resources(app, config)

    user_service(app, config, '/user')

    music_platforms(app, config, '/music')

    core_functions(app, config, '/core')


def static_resources(app, config: dict, prefix=''):
    '''
    static resources
    '''
    app.router.add_static('/kris/', path='front/admin/', name='admin', show_index=True)

    app.router.add_static('/resource/', path='core/resources', name='resource', show_index=True)


def core_functions(app, config: dict, prefix=''):
    '''
    core functions
    '''
    core = Cores(config)

    # extract music from mv
    app.router.add_post(url(prefix, '/extract'), core.extractAudio)

    # start download
    app.router.add_post(url(prefix, '/download'), core.downloadRes)

    # get download progress
    app.router.add_get(url(prefix, '/download/progress'), core.dlProgress)


def user_service(app, config: dict, prefix=''):
    '''
    user service
    '''
    user = Users(config)

    # user login
    app.router.add_post(url(prefix, '/login'), user.login)

    # user sign up
    app.router.add_post(url(prefix, '/sign'), user.signUp)

    # user love a song, add song to his list
    app.router.add_post(url(prefix, '/love/song'), user.loveSong)

    # get user loved songs
    app.router.add_get(url(prefix, '/loved/songs'), user.getUserLove)

    # user dislike a song, remove song from his list
    app.router.add_post(url(prefix, '/hate/song'), user.hateSong)

    # update user's info
    app.router.add_post(url(prefix, '/info/update'), user.update)

    # upload avator
    app.router.add_post(url(prefix, '/upload/avator'), user.uploadAvator)


def music_platforms(app, config: dict, prefix=''):
    '''
    controllers for music platforms' services
    '''
    platforms = Platforms(config)

    # search and return song
    app.router.add_get(url(prefix, '/{platform}/songs'), platforms.searchSong)

    # search and return album
    app.router.add_get(url(prefix, '/{platform}/albums'), platforms.searchAlbum)

    # search and return mv
    app.router.add_get(url(prefix, '/{platform}/mv'), platforms.searchMV)

    # get songs in an album
    app.router.add_get(url(prefix, '/{platform}/songs/album'), platforms.songsinAlbum)

    # get songs in a user songlist
    app.router.add_get(url(prefix, '/{platform}/songs/songlist'), platforms.songsinSonglist)

    # get comments of a song
    app.router.add_get(url(prefix, '/{platform}/comments/song'), platforms.commentsSong)

    # get comments of a album
    app.router.add_get(url(prefix, '/{platform}/comments/album'), platforms.commentsAlbum)

    # get comments of a mv
    app.router.add_get(url(prefix, '/{platform}/comments/mv'), platforms.commentsMV)

    # get lyric of a song
    app.router.add_get(url(prefix, '/{platform}/lyric/{id}'), platforms.lyric)

    # redirect to an effective uri of a song
    app.router.add_get(url(prefix, '/{platform}/song/{id}'), platforms.song)

    # get uri of a song
    app.router.add_get(url(prefix, '/{platform}/uri/song'), platforms.songUri)

    # get uri of a mv
    app.router.add_get(url(prefix, '/{platform}/uri/mv'), platforms.mvUri)

    # get user's public songlists
    app.router.add_get(url(prefix, '/{platform}/user/songlists'), platforms.userSonglists)

    # redirect pic
    app.router.add_get(url(prefix, '/{platform}/albumcover/{id}'), platforms.albumPic)

    # redirect pic
    app.router.add_get(url(prefix, '/redirect/{platform}/{id:.+}'), platforms.redirect)

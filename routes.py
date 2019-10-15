'''
    setup routes
'''
from services import register_services


def setup_routes(app):

    # register services
    core, user, platform = register_services()

    # index html
    app.router.add_get('/', core.index)

    # return frontend static files
    app.router.add_get('/static/{filename}', core.static)

    # return media file resource
    app.router.add_get('/resource/{ftype}/{fname}', core.getResource)

    # extract music from mv
    app.router.add_post('/extract', core.extractAudio)

    '''
    Creepers from platform
    '''

    # search and return song
    app.router.add_get('/{platform}/songs', platform.searchSong)

    # search and return album
    app.router.add_get('/{platform}/albums', platform.searchAlbum)
    
    # search and return mv
    app.router.add_get('/{platform}/mv', platform.searchMV)

    # get songs in an album
    app.router.add_get('/{platform}/songs/album', platform.songsinAlbum)

    # get songs in a user songlist
    app.router.add_get('/{platform}/songs/songlist', platform.songsinSonglist)

    # get comments of a song
    app.router.add_get('/{platform}/comments/song', platform.commentsSong)

    # get comments of a album
    app.router.add_get('/{platform}/comments/album', platform.commentsAlbum)

    # get comments of a mv
    app.router.add_get('/{platform}/comments/mv', platform.commentsMV)

    # get lyric of a song
    app.router.add_get('/{platform}/lyric/{id}', platform.lyric)
    
    # redirect to an effective uri of a song
    app.router.add_get('/{platform}/song/{id}', platform.song)
    
    # get uri of a song
    app.router.add_get('/{platform}/uri/song', platform.songUri)

    # get uri of a mv
    app.router.add_get('/{platform}/uri/mv', platform.mvUri)

    # get user's public songlists
    app.router.add_get('/{platform}/user/songlists', platform.userSonglists)

    # redirect pic
    app.router.add_get('/{platform}/albumcover/{id}', platform.albumPic)

    '''
        local service
    '''

    # user login
    app.router.add_post('/login', user.login)
    
    # user sign up
    app.router.add_post('/sign', user.signUp)

    # user love a song, add song to his list
    app.router.add_post('/user/love/song', user.loveSong)

    # get user loved songs
    app.router.add_get('/user/loved/songs', user.getUserLove)

    # user dislike a song, remove song from his list
    app.router.add_post('/user/hate/song', user.hateSong)
from views import *

def setup_routes(app):
    # index html
    app.router.add_get('/', index)

    # return frontend static files
    app.router.add_get('/static/{filename}', files)

    # return media file resource
    app.router.add_get('/resource/{ftype}/{fname}', getResource)

    # search and return song
    app.router.add_get('/{platform}/songs', searchSong)

    # search and return album
    app.router.add_get('/{platform}/albums', searchAlbum)
    
    # search and return mv
    app.router.add_get('/{platform}/mv', searchMV)

    # get songs in an album
    app.router.add_get('/{platform}/songs/album', songsinAlbum)

    # get songs in a user songlist
    app.router.add_get('/{platform}/songs/songlist', songsinSonglist)

    # get comments of a song
    app.router.add_get('/{platform}/comments/song', commentsSong)

    # get comments of a album
    app.router.add_get('/{platform}/comments/album', commentsAlbum)

    # get comments of a mv
    app.router.add_get('/{platform}/comments/mv', commentsMV)

    # get lyric of a song
    app.router.add_get('/{platform}/lyric/{id}', lyric)
    
    # redirect to an effective uri of a song
    app.router.add_get('/{platform}/song/{id}', song)
    
    # get uri of a song
    app.router.add_get('/{platform}/uri/song', songUri)

    # get uri of a mv
    app.router.add_get('/{platform}/uri/mv', mvUri)

    # get user's public songlists
    app.router.add_get('/{platform}/user/songlists', userSonglists)

    # redirect pic
    app.router.add_get('/{platform}/albumcover/{id}', albumPic)

    '''
        local service
    '''

    # user login
    app.router.add_post('/login', login)
    
    # user sign up
    app.router.add_post('/sign', signUp)

    # user love a song, add song to his list
    app.router.add_post('/user/love/song', loveSong)

    # get user loved songs
    app.router.add_get('/user/loved/songs', getUserLove)

    # user dislike a song, remove song from his list
    app.router.add_post('/user/hate/song', hateSong)

    # extract music from mv
    app.router.add_post('/extract', extractAudio)
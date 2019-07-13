from views import *

def setup_routes(app):
    # index html
    app.router.add_get('/', index)

    # return static files
    app.router.add_get('/static/{filename}', files)

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
    
    # get uri of a song
    app.router.add_get('/{platform}/uri/song', songUri)

    # get uri of a mv
    app.router.add_get('/{platform}/uri/mv', mvUri)

    # get user's public songlists
    app.router.add_get('/{platform}/user/songlists', userSonglists)

    # redirect pic
    app.router.add_get('/{platform}/albumcover/{id}', albumPic)

    # test dynamic router
    app.router.add_get('/{platform}/test/dynamic', testDynamic)
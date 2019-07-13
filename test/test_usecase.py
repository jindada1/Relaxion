from aiohttp import web
from routes import setup_routes
import json

# pip install pytest-aiohttp
# !!! require python version 3.7 or 3.5.3  !!!
def create_app(loop):
    app = web.Application(loop=loop)
    setup_routes(app)
    return app

async def test_run_server(test_client, loop):
    api = await test_client(create_app)
    resp = await api.get('/')
    assert resp.status == 200

async def test_s_s_ps_sc_pm_mc(test_client, loop):
    print("\n test_search_song_playMusic_getSongComments_playmv_getMVComments")
    api = await test_client(create_app)
    # search 周杰伦
    resp = await api.get('/search/song',params={"searchkey":"周杰伦"})
    songs = json.loads(await resp.text())['songs']
    if len(songs):
        assert True
        print("search songs success")
        song = songs[0]

        resp = await api.get('/comments',params={"idforcomments":song["idforcomments"],"type":"song"})
        comments = json.loads(await resp.text())['normal']['comments']
        if len(comments):
            assert True
            print("get comments of song success")

        resp = await api.get('/song',params={"idforres":song["idforres"]})
        uri = json.loads(await resp.text())['uri']
        if uri:
            assert True
            print("get music uri success")

        resp = await api.get('/lyric',params={"idforres":song["idforres"]})
        if await resp.text():
            assert True
            print("get music lyric success")

        resp = await api.get('/mv',params={"mvid":song["mvid"]})
        uri = json.loads(await resp.text())['uri']
        if uri:
            assert True
            print("get mv uri success")

        resp = await api.get('/comments',params={"idforcomments":song["mvid"],"type":"mv"})
        comments = json.loads(await resp.text())['normal']['comments']
        if len(comments):
            assert True
            print("get comments of mv success")


async def test_search_mv_playmv_getMVComments(test_client):
    print("\n test_search_mv_playmv_getMVComments")
    api = await test_client(create_app)
    # search 周杰伦
    resp = await api.get('/search/mv',params={"searchkey":"周杰伦"})
    videos = json.loads(await resp.text())['videos']
    if len(videos):
        assert True
        print("search videos success")
        video = videos[0]

        resp = await api.get('/mv',params={"mvid":video["mvid"]})
        uri = json.loads(await resp.text())['uri']
        if uri:
            assert True
            print("get mv uri success")

        resp = await api.get('/comments',params={"idforcomments":video["idforcomments"],"type":"mv"})
        comments = json.loads(await resp.text())['normal']['comments']
        if len(comments):
            assert True
            print("get comments of mv success")


async def test_s_a_dm_ac_pm_mc(test_client):
    print("\n test_search_album_displayMusics_getAlbumComments_playMusic_getMusicComments")
    api = await test_client(create_app)
    # search 周杰伦
    resp = await api.get('/search/album',params={"searchkey":"周杰伦"})
    albums = json.loads(await resp.text())['albums']
    if len(albums):
        assert True
        print("search albums success")
        album = albums[0]

        resp = await api.get('/songs/album',params={"albumid":album["albumid"]})
        songs = json.loads(await resp.text())['songs']
        if len(songs):
            assert True
            print("get songs in album success")

        resp = await api.get('/comments',params={"idforcomments":album["idforcomments"],"type":"album"})
        comments = json.loads(await resp.text())['normal']['comments']
        if len(comments):
            assert True
            print("get comments of album success")

        song = songs[0]

        resp = await api.get('/song',params={"idforres":song["idforres"]})
        uri = json.loads(await resp.text())['uri']
        if uri:
            assert True
            print("get music uri success")

        resp = await api.get('/comments',params={"idforcomments":song["idforcomments"],"type":"song"})
        comments = json.loads(await resp.text())['normal']['comments']
        if len(comments):
            assert True
            print("get comments of song success")


async def test_getusersonglists_displaymusics_playmusic(test_client):
    print("\n test_getusersonglists_displaymusics_playmusic")
    api = await test_client(create_app)
    # search 周杰伦
    resp = await api.get('/user/songlists',params={"userid":"406143883"})
    lists = json.loads(await resp.text())['allLists']
    if len(lists):
        assert True
        print("search user lists success")

        _list = lists[0]
        resp = await api.get('/songs/songlist',params={"dissid":_list["dissid"]})
        songs = json.loads(await resp.text())['songs']
        if len(songs):
            assert True
            print("get songs in album success")
        
        song = songs[0]
        resp = await api.get('/song',params={"idforres":song["idforres"]})
        uri = json.loads(await resp.text())['uri']
        if uri:
            assert True
            print("get music uri success")
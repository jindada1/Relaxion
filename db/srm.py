try:
    from .users import userAdapter
    from .songs import songAdapter
    from .playlists import listAdapter
    from .adapter import connect
except:
    from users import userAdapter
    from songs import songAdapter
    from playlists import listAdapter
    from adapter import connect

import json


class dbService(object):
    def __init__(self, dbfile):
        conn = connect(dbfile)
        if conn:
            self.users = userAdapter(conn, 'userinfo')
            self.songs = songAdapter(conn, 'song')
            self.songlist = listAdapter(conn, 'playlist')
        

    def register(self, user):
        user['info'] = '{}'

        if self.users.insert(user):
            return {'succ': 'ok'}
            
        return {'err': 'exist'}

    def login(self, user):

        pw = self.users.find_property(user['name'], 'pw')
        if not pw:
            return {'err': 'no user'}

        if user['pw'] == pw:
            info = self.users.find_property(user['name'], 'info')
            return {
                "name": user['name'],
                "pw": pw,
                "info": json.loads(info)
            }

        return {'err': 'password error'}

    def update(self, user):
        
        user['info'] = json.dumps(user['info'])
        return self.users.update(user)

    def get_songlist(self, userid):

        ids = self.songlist.fetch_all(userid)
        songs = []

        for songid in ids:
            info_json_str = self.songs.find_property(songid, 'info')
            try:
                songs.append(json.loads(info_json_str))

            # if this info is invalid, remove this record from database
            except:
                self.hate_song(userid, songid)

        return songs

    def love_song(self, userid, songid, info_str):

        if self.songlist.insert(userid, songid):

            # store this song
            self.songs.insert(songid, info_str)

            # loved count ++
            num = self.songs.find_property(songid, 'count')
            self.songs.update_property(songid, ("count", num + 1))

            return True

        return False

    def hate_song(self, userid, songid):
        return self.songlist.delete(userid, songid)

    def get_videolist(self, userid):
        pass

    def love_video(self, userid, songid):
        pass

    def hate_video(self, userid, songid):
        pass


if __name__ == '__main__':
    
    import os, sys

    dbf = os.path.join(sys.path[0], "User.db")
    
    localdb = dbService(dbf)
    
    # √ print(localdb.get_songlist('Kris'))
    # √ print(localdb.login({'name':'听说你锁了','pw':'1234'}))
    # √ print(localdb.register({'name':'Kun','pw':'1234'}))
    # √ print(localdb.love_song('Kris','test','test'))

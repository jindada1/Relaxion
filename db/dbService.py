try:
    from .userAdapter import userAdapter
    from .listAdapter import listAdapter
    from .songAdapter import songAdapter
except:
    from userAdapter import userAdapter
    from listAdapter import listAdapter
    from songAdapter import songAdapter

import json


class dbService(object):
    def __init__(self, dbfile):
        self.users = userAdapter(dbfile, 'userinfo')
        self.songs = songAdapter(dbfile, 'song')
        self.songlist = listAdapter(dbfile, 'playlist')

    def register(self, user):
        user['info'] = '{}'

        if self.users.insert(user):
            return {'succ': 'ok'}
            
        return {'err': 'exist'}

    def login(self, user):

        pw = self.users.find_property(user['name'], 'pw')
        if not pw:
            return {'err': 'no-user'}

        if user['pw'] == pw:
            info = self.users.find_property(user['name'], 'info')
            return json.loads(info)

        return {'err': 'password-error'}

    def bind_info(self, user):

        return self.users.update(user)

    def get_songlist(self, userid):

        ids = self.songlist.fetch_all(userid)
        songs = []

        for songid in ids:
            info_json_str = self.songs.find_property(songid, 'info')
            if info_json_str:
                songs.append(json.loads(info_json_str))

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
    localdb = dbService('User.db')
    # √ print(localdb.get_songlist('Kris'))
    # √ print(localdb.login({'name':'Kris','pw':'1234'}))

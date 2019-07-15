
from .userAdapter import userAdapter
from .listAdapter import listAdapter
from .songAdapter import songAdapter

class dbService(object):
    def register(self, user):
        pass
    
    def login(self, user):
        pass

    def bind_info(self, user):
        pass

    def get_songlist(self, userid):
        pass

    def love_song(self,userid, songid):
        pass

    def hate_song(self, userid, songid):
        pass

    def get_videolist(self, userid):
        pass

    def love_video(self,userid, songid):
        pass

    def hate_video(self, userid, songid):
        pass

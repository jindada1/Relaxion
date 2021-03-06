'''
handle the operation on song info and download
'''


try:
    from .adapter import dbAdapter
except:
    from adapter import dbAdapter


class songAdapter(dbAdapter):

    def __init__(self, db, table):

        super().__init__(db, table)
        
        self.table = table

    def insert(self, songid, info):
        try:
            self.sql_do('insert into {} (songid, info, count) values (?, ?, ?)'.format(
                self.table), (songid, info, 1,))
            return True
        except:
            return False

    def fetch_row(self, key):

        t_res = self.retrive(
            'select * from {} where songid = ?'.format(self.table), (key,))

        if t_res:
            return {
                "songid": t_res[0],
                "info": t_res[1],
                "count": t_res[2]
            }
        # no row
        return None

    def find_property(self, key, prop):

        t_res = self.retrive(
            'select {0} from {1} where songid = ?'.format(prop, self.table), (key,))

        if t_res:
            return t_res[0]
        # no row
        return None

    def update_property(self, key, prop_value):

        rows = self.sql_do('update {} set {} = ? where songid = ?'.format(
            self.table, prop_value[0]), (prop_value[1],key,))

        return rows

    def delete(self, key):

        rows = self.sql_do(
            'delete from {} where songid = ?'.format(self.table), (key,))

        return rows

    def add_media(self, key, url):
        pass


if __name__ == '__main__':
    
    import json

    db = 'User.db'
    table = 'song'
    songs = songAdapter(db, table)


    songsdata = [
        {
            "songid": "qq123",
            'info': json.dumps({
                "name": "告白气球",
                "singer": "周杰伦"
            },ensure_ascii=False)
        },
        {
            "songid": "qq123wtf",
            'info': json.dumps({
                "name": "等你下课",
                "singer": "周杰伦"
            },ensure_ascii=False)
        }
    ]

    for song in songsdata:
        print(songs.insert(song['songid'], song['info']))
    # print(songs.fetch_row(song['songid']))
    # num = songs.find_property(song['songid'], 'count')
    # print(songs.update_property(song['songid'],("count", num + 1)))
    # print(songs.delete(song['songid']))
    songs.disp_table()

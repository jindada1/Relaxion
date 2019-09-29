'''
handle the operation on user's playlist
'''

try:
    from .dbAdapter import dbAdapter
except:
    from dbAdapter import dbAdapter



class listAdapter(dbAdapter):

    def __init__(self, db, table):

        super().__init__(db, table)

        self.table = table

    def insert(self, username, songid):
        try:
            self.sql_do('insert into {} (username, songid, id) values (?, ?, ?)'.format(
                self.table), (username, songid, username + songid))
            return True
        except:
            return False

    def fetch_all(self, key):

        t_res = self.retrive_all(
            'select * from {} where username = ?'.format(self.table), (key,))

        return list(map(lambda x: x[1], t_res))

    def delete(self, username, songid):

        rows = self.sql_do(
            'delete from {} where id = ?'.format(self.table), (username + songid,))

        return rows


if __name__ == '__main__':

    db = 'User.db'
    table = 'playlist'
    records = listAdapter(db, table)

    record = [
        {
            'username': 'Kris',
            'songid': 'qq123',
        },
        {
            'username': 'Kris',
            'songid': 'qq123wtf',
        }
    ]


    for r in record:
        print(records.insert(r['username'], r['songid']))
    
    # print(records.fetch_all('Kris'))
    # print(records.delete(record[0]))
    # records.disp_table()

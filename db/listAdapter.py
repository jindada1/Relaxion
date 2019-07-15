'''
handle the operation on user's playlist
'''

try:
    from .dbAdapter import dbAdapter
except:
    from dbAdapter import dbAdapter



class listAdapter(dbAdapter):

    def __init__(self, db, table):

        super().__init__(db)
        print(table)
        self.table = table

    def insert(self, row):
        try:
            self.sql_do('insert into {} (username, songid, id) values (?, ?, ?)'.format(
                self.table), (row['username'], row['songid'],row['username'] + row['songid']))
            return True
        except:
            return False

    def fetch_all(self, key):

        t_res = self.retrive_all(
            'select * from {} where username = ?'.format(self.table), (key,))

        return list(map(lambda x: x[1], t_res))

    def delete(self, row):

        rows = self.sql_do(
            'delete from {} where id = ?'.format(self.table), (row['username'] + row['songid'],))

        return rows


if __name__ == '__main__':

    db = 'User.db'
    table = 'playlist'
    records = listAdapter(db, table)

    record = [
        {
            'username': 'Kris',
            'songid': '1234',
        },
        {
            'username': 'Kris',
            'songid': '1235',
        },
        {
            'username': 'Kris',
            'songid': '2563',
        }
    ]


    for r in record:
        print(records.insert(r))
    
    print(records.fetch_all('Kris'))
    print(records.delete(record[0]))
    # records.disp_table()

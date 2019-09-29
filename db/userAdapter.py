try:
    from .dbAdapter import dbAdapter
except:
    from dbAdapter import dbAdapter


class userAdapter(dbAdapter):

    def __init__(self, db, table):

        super().__init__(db, table)
        
        self.table = table

    def insert(self, row):
        try:
            self.sql_do('insert into {} (name, pw, info) values (?, ?, ?)'.format(
                self.table), (row['name'], row['pw'], row['info'],))
            return True
            
        except:
            return False

    def fetch_row(self, key):

        t_res = self.retrive(
            'select * from {} where name = ?'.format(self.table), (key,))

        if t_res:
            return {
                "name": t_res[0],
                "pw": t_res[1],
                "info": t_res[2]
            }
        # no row
        return None

    def find_property(self, key, prop):

        t_res = self.retrive(
            'select {0} from {1} where name = ?'.format(prop, self.table), (key,))

        if t_res:
            return t_res[0]
        # no row
        return None

    def update(self, row):

        rows = self.sql_do('update {} set pw = ?,info = ? where name = ?'.format(
            self.table), (row['pw'], row['info'], row['name'],))

        return rows

    def delete(self, key):

        rows = self.sql_do(
            'delete from {} where name = ?'.format(self.table), (key,))

        return rows


if __name__ == '__main__':
    
    import json

    db = 'User.db'
    table = 'userinfo'
    users = userAdapter(db, table)

    user = {
        'name': 'Kris',
        'pw': '1234',
        'info': json.dumps({
            "qq": {
                "number": "406143883"
            }
        },ensure_ascii=False)
    }

    # print(users.insert(user))
    # print(users.update(user))
    # print(users.fetch_row('Kris'))
    # print(users.find_property('Kris','info'))
    # print(users.delete('12354'))
    
    users.disp_table()

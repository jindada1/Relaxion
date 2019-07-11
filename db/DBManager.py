import sqlite3

DB_FILE = './Caches.db'


def __disPlayAllMusicQualities():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM SONGQUALITIES");
    result = c.fetchall()
    conn.commit()
    conn.close()
    print('SONGMID   QUALITY    TIME')
    for r in result:
        print(r)
    return result

def __createTable():
    conn = sqlite3.connect(DB_FILE)
    print("Opened database successfully");
    c = conn.cursor()
    c.execute('''CREATE TABLE QQUSER
            (QQNUM     CHAR(20)   PRIMARY KEY     NOT NULL,
             USERID    CHAR(20)   NOT NULL);''')
    print("Table created successfully");
    conn.commit()
    conn.close()

def __disPlayAllQQUSER():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM QQUSER");
    result = c.fetchall()
    conn.commit()
    conn.close()
    print('QQNUM   USERID')
    for r in result:
        print(r)
    return result

def __disPlayAllQQLyric():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM QQLyric");
    result = c.fetchall()
    conn.commit()
    conn.close()
    print('SONGMID   LYRIC')
    for r in result:
        print(r)
    return result

def __dropTable(table):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DROP TABLE " + table)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    __disPlayAllMusicQualities()
    __disPlayAllQQLyric()
    __disPlayAllQQUSER()
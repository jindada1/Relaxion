import sqlite3

DB_FILE = './db/Caches.db'

'''
table 1:-----------------------------------------------------

<name> : SONGQUALITIES
<declare>  <schema>       <type>     <tyle>     <testvalue>
  PKEY     [SONGMID]      CHAR(20)   NOTNULL   'testsongmid'
           [QUALITY]      INT        NOTNULL   
           [TIME   ]      INT        NOTNULL   
-------------------------------------------------------------

table 2:-----------------------------------------------------

<name> : QQLyric
<declare>  <schema>       <type>     <tyle>     <testvalue>
  PKEY     [SONGMID]      CHAR(20)   NOT NULL  'testsongmid'
           [LYRIC]        TEXT       NOT NULL   
-------------------------------------------------------------

table 2:-----------------------------------------------------

<name> : QQUSER
<declare>  <schema>       <type>     <tyle>     <testvalue>
  PKEY     [QQNUM]      CHAR(20)     NOT NULL   '406143883'
           [USERID]     CHAR(20)     NOT NULL   
-------------------------------------------------------------

'''


def getMusicQuality(songmid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT QUALITY, TIME from SONGQUALITIES where SONGMID=?", (songmid,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return {'quality':1,'time':0}
    return {'quality':result[0],'time':result[1]}

def updateMusicQuality(songmid,quality,time):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE SONGQUALITIES set TIME = ?,QUALITY = ? where SONGMID=?",(time,quality,songmid,))
    conn.commit()
    conn.close()

def addMusicQuality(songmid,quality,time):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO SONGQUALITIES (SONGMID,QUALITY,TIME)  VALUES (?, ?, ?)",(songmid,quality,time,));
    conn.commit()
    conn.close()

def deleteMusicQuality(songmid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE from SONGQUALITIES where SONGMID=?;",(songmid,))
    conn.commit()
    conn.close()

def addQQLyric(songmid,lyric):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO QQLyric (SONGMID,LYRIC)  VALUES (?, ?)",(songmid,lyric,));
    conn.commit()
    conn.close()

def getLyric(songmid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT LYRIC from QQLyric where SONGMID=?", (songmid,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return False
    return result[0]

def addQQUserid(qqnum,userid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO QQUSER (QQNUM,USERID)  VALUES (?, ?)",(qqnum,userid,));
    conn.commit()
    conn.close()

def getQQUserid(qqnum):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT USERID from QQUSER where QQNUM=?", (qqnum,))
    result = c.fetchone()
    conn.close()
    if result is None:
        return False
    return result[0]

if __name__ == '__main__':
    pass
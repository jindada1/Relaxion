
'''
on  :  2019-07-14
by  :  Kris Huang

for : 
    Create a wrapper around the sqlite3 python library, which includes basic CRUD operations 
    and other utility functions 

refer : 
    https://gist.github.com/goldsborough/c973d934f620e16678bf
    https://github.com/hassanazimi/Python/blob/master/16%20Databases/sqlite3-class.py

'''

import sqlite3

def connect(dbfile):
    try:
        conn = sqlite3.connect(dbfile)
        # cursor = self.conn.cursor()
        print("[ok] connect db file %s" % dbfile)
        return conn

    except sqlite3.Error as e:
        print("[err] %s" % e)
        return None

class dbAdapter(object):
    def __init__(self, conn, table=None):
        self.conn = conn
        self.cursor = conn.cursor()

        if table:
            self.cursor.execute('select * from {}'.format(table))
            print("[ok] find table:%s" % table)


    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_value, traceback):

        self.close()

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    # execute sql commands
    def sql_do(self, sql, params):
        
        print(sql, params)

        self.cursor.execute(sql, params)
        self.conn.commit()

        # will be 1 if the update was successful (affecting 1 row) or 0 if it failed
        return self.cursor.rowcount

    def retrive(self, sql, params):

        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def retrive_all(self, sql, params):

        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def disp_table(self):

        self.cursor.execute(
            'select * from {}'.format(self.table))

        for row in self.cursor:
            print(row)

    #######################################################################
    #
    # Function to fetch/query data from a database.
    #
    #  This is the main function used to query a database for data.
    #
    #  @param table The name of the database's table to query from.
    #
    #  @param columns The string of columns, comma-separated, to fetch.
    #
    #  @param limit Optionally, a limit of items to fetch.
    #
    #######################################################################

    def get(self, table, columns, limit=None):

        query = "SELECT {0} from {1};".format(columns, table)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()

        return rows[len(rows)-limit if limit else 0:]

    #######################################################################
    #
    # Utility function that summarizes a dataset.
    #
    #  This function takes a dataset, retrieved via the get() function, and
    #  returns only the maximum, minimum and average for each column.
    #
    #  @param rows The retrieved data.
    #
    #######################################################################

    @staticmethod
    def summary(rows):

        # split the rows into columns
        cols = [[r[c] for r in rows] for c in range(len(rows[0]))]

        # the time in terms of fractions of hours of how long ago
        # the sample was assumes the sampling period is 10 minutes
        def t(col): return "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        ret = []

        for c in cols:
            hi = max(c)
            hi_t = t(c.index(hi))

            lo = min(c)
            lo_t = t(c.index(lo))

            avg = sum(c)/len(rows)

            ret.append(((hi, hi_t), (lo, lo_t), avg))

        return ret

    #######################################################################
    #
    # Utility function that converts a dataset into CSV format.
    #
    #  @param data The data, retrieved from the get() function.
    #
    #  @param fname The file name to store the data in.
    #
    #  @see get()
    #
    #######################################################################

    @staticmethod
    def toCSV(data, fname="output.csv"):

        with open(fname, 'a') as file:
            file.write(",".join([str(j) for i in data for j in i]))

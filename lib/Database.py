import pymysql


class Database:
    db = None
    sth = None

    def __init__(self):
        self.connect_db()  # Connect

    def get_cursor(self):
        return self.db.cursor(pymysql.cursors.DictCursor)

    def connect_db(self):
        self.db = pymysql.connect(host="localhost",
                                  user="root",
                                  passwd="super9server",
                                  db="gameCentral")
        self.sth = self.get_cursor()  # Get the cursor

    def query(self, sql, params=None):
        return self.sth.execute(sql, params)

    def fetch(self):
        return self.sth.fetchone()

    def fetch_all(self):
        return self.sth.fetchall()

    def last_insert(self):
        return self.sth.lastrowid

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def close(self):
        self.db.close()

    def rowcount(self):
        return self.sth.rowcount
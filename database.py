import sqlite3
from sqlite3 import Error
from datetime import datetime


class database:
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger
        self.initialise_db()

    def db_connection(self):
        con = None
        try:
            con = sqlite3.connect(str(self.name) + ".db")
            # self.logger.info("Connected to finelady.db", sqlite3.version)
        except Error as e:
            # self.logger.info(e)
            print(e)

        return con

    def initialise_db(self):
        # Create user opt-out table
        user_opt_out_sql = """CREATE TABLE IF NOT EXISTS opt_out_users (
                id integer PRIMARY KEY,
                username text UNIQUE NOT NULL,
                request_date timestamp
                );"""

        # Create sub opt-out table
        sub_opt_out_sql = """CREATE TABLE IF NOT EXISTS opt_out_subs (
                id integer PRIMARY KEY,
                subreddit text UNIQUE NOT NULL,
                requestor text,
                request_date timestamp
                );"""

        for query in [user_opt_out_sql, sub_opt_out_sql]:
            self.create_table(query)

    def create_table(self, sql, args=False):
        with self.db_connection() as con:
            cur = con.cursor()
            if args:
                cur.execute(sql, args)
            else:
                cur.execute(sql)

    def add_opt_out_user(self, name, request_date):
        sql = """INSERT OR IGNORE INTO opt_out_users(username, request_date)
        VALUES(?,?);"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql, (name, request_date))

    def add_opt_out_sub(self, subreddit, requestor, request_date):
        sql = """INSERT OR IGNORE INTO opt_out_users(subreddit, requestor, request_date)
        VALUES(?,?,?);"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql, (subreddit, requestor, request_date))

    def query_users(self):
        sql = """SELECT username FROM opt_out_users"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql)
            users = cur.fetchall()
            return [user[0] for user in users]

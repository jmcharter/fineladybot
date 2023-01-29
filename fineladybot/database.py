import sqlite3
from sqlite3 import Error
from datetime import datetime
from pathlib import Path
from logging import Logger
from typing import Optional

filepath = Path(__file__).parent.absolute()


class Database:
    def __init__(self, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.initialise_db()

    def db_connection(self) -> sqlite3.Connection:
        con: sqlite3.Connection
        try:
            con = sqlite3.connect(str(filepath.joinpath(self.name)) + ".db")
            # self.logger.info("Connected to finelady.db\nSQLite3 version %s", sqlite3.version)
        except Error as e:
            self.logger.info(e)

        return con

    def initialise_db(self) -> None:
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
            self._create_table(query)

    def _create_table(self, sql: str, args: Optional[str] = None) -> None:
        with self.db_connection() as con:
            cur = con.cursor()
            if args:
                cur.execute(sql, args)
            else:
                cur.execute(sql)

    def add_opt_out_user(self, name: str, request_date: datetime) -> None:
        sql = """INSERT OR IGNORE INTO opt_out_users(username, request_date)
        VALUES(?,?);"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql, (name, request_date))

    def add_opt_out_sub(self, subreddit: str, requestor: str, request_date: datetime) -> None:
        sql = """INSERT OR IGNORE INTO opt_out_subs(subreddit, requestor, request_date)
        VALUES(?,?,?);"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql, (subreddit, requestor, request_date))

    def query_users(self) -> list[str]:
        sql = """SELECT username FROM opt_out_users"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql)
            users = cur.fetchall()
            return [user[0] for user in users]

    def query_subs(self) -> list[str]:
        sql = """SELECT subreddit FROM opt_out_subs"""
        with self.db_connection() as con:
            cur = con.cursor()
            cur.execute(sql)
            subs = cur.fetchall()
            return [sub[0] for sub in subs]

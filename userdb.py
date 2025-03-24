"""
BEAU ALBRITTON 
TODO: REFACTOR USERDB FOR 'AUTHENTIC' CODE (WRITTEN WITH MY HANDS ONLY!)
NOTE: SLIGHTLY MODIFIED DB.PY FILE FROM CATAMOUNT COMMUNITY BANK, 
ALL CREDIT TO JIM EDDY AND CATAMOUNT COMMUNITY BANK ON GITLAB

This file includes a simple database class, which provides methods:

    execute_query:  Takes a query as a string and executes it with a current
                    database connection. Doing things this way is not advised,
                    since it introduces vulnerability to injection attack.
                    We do it this way for instructional purposes only!

    setup:          A utility to create a fresh instance of the database,
                    and to populate it with some records for testing.

Here we use SQLite directly rather than an ORM (object relational mapper, e.g.,
SQLAlchemy) because it's easier for students to see what's going on in SQL
queries.
"""

import os
import json
from typing import Union
import sqlite3
import config


class Db:
    """Database class for user login environment. """

    # SQL query to create new `users` table
    CREATE_TABLE_USER = """CREATE TABLE users (
        id integer PRIMARY KEY,
        username text NOT NULL UNIQUE,
        pwhash text NOT NULL,
        role text NOT NULL
    );"""
    #Modified insert for users table
    INSERT_USER = """INSERT INTO users
        (id, username, pwhash, role)
        VALUES("{id}", "{username}", "{pwhash}", "{role}");"""

    #defining error to be read in for potential registration/login problems.
    ERROR = sqlite3.Error

    #Rest is pretty much unchanged
    @staticmethod
    def get_connection():
        """
        Get a connection to the database
        :return: sqlite3.Connection
        """
        return sqlite3.connect(config.DB_FILE)

    @staticmethod
    def execute_query(cnx: sqlite3.Connection, query: str):
        """
        Execute a SQL query. This method takes a connection to the database
        and executes a query passed in as a string.
        :param cnx: sqlite3.Connection
        :param query: str
        """
        c = cnx.cursor()
        if config.SC in query:
            c.executescript(query)
        else:
            c.execute(query)
        cnx.commit()
        return c

    @classmethod
    def setup(cls) -> Union[sqlite3.Connection, None]:
        """
        Setup the database tables
        """
        try:
            os.remove(config.DB_FILE)
        except FileNotFoundError:
            pass
        try:
            cnx = cls.get_connection()
            cls.execute_query(cnx, cls.CREATE_TABLE_USER)
            cls._populate_users(cnx)
            c = cls.list_tables(cnx)
            rows = c.fetchall()
            assert ('users',) in rows
            return cnx  # Because maybe you want to reuse it
        except sqlite3.Error as e:
            print("An error has occurred. Please report this incident.")
            print(e)
            return None

    @classmethod
    def list_tables(cls, cnx: sqlite3.Connection):
        """
        List tables
        :param cnx:
        :return:
        """
        q = "SELECT name FROM sqlite_master WHERE type ='table' " \
            "AND name NOT LIKE 'sqlite_%'"
        c = cls.execute_query(cnx, q)
        return c

    @classmethod
    def _populate_users(cls, cnx: sqlite3.Connection):
        """
        Populate user table with records from JSON file. Yes, we could do
        this more efficiently. Suffices for our purposes.
        :param cnx: sqlite3.Connection
        """
        with open('./data/users.json', 'r') as f:
            data = json.load(f)
        for record in data['RECORDS']:
            query = cls.INSERT_USER.format(
                id=record['id'],
                username=record['username'],
                pwhash=record['pwhash'],
                role=record['role']
            )
            # print(query)
            c = cls.execute_query(cnx, query)
        return c
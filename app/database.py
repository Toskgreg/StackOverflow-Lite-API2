"""This module handles database queries"""
from urllib.parse import urlparse
import psycopg2
from werkzeug.security import generate_password_hash
from flask import current_app as app


class Database:
    """This class does all database related stuff"""

    def __init__(self, database_url):
        """Initializes the connection url"""
        parsed_url = urlparse(database_url)
        d_b = parsed_url.path[1:]
        username = parsed_url.username
        hostname = parsed_url.hostname
        password = parsed_url.password
        port = parsed_url.port

        self.conn = psycopg2.connect(
            database=d_b, user=username, password=password,
            host=hostname, port=port)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_database(self, db_name):
        """Creates a database to be used in production"""
        self.cur.execute('CREATE DATABASE {};'.format(db_name))

    def create_tables(self):
        """Creates database tables """
        create_table = "CREATE TABLE IF NOT EXISTS users\
        (id SERIAL PRIMARY KEY, name text, username text, password text)"
        self.cur.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS questions\
        (id SERIAL PRIMARY KEY, title text, description1\
        text, date TIMESTAMP NOT NULL, posted_by text)"
        self.cur.execute(create_table)


    def trancate_table(self, table):
        """Trancates the table"""
        self.cur.execute("TRUNCATE TABLE {} RESTART IDENTITY".format(table))

    def fetch_by_param(self, table_name, column, param):
        """Fetches a single a parameter from a specific table and column"""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            table_name, column, param)
        self.cur.execute(query)
        row = self.cur.fetchone()
        return row

class UserBbQueries(Database):
    """This class handles database transactions for the user"""

    def __init__(self):
        Database.__init__(self, app.config['DATABASE_URL'])

    def insert_user_data(self, data):
        query = "INSERT INTO users (name, username, password)\
            VALUES('{}','{}', '{}');".format(data['name'],
                                             data['username'],
                                             generate_password_hash
                                             (data['password']))
        self.cur.execute(query)
        self.conn.commit()


class QuestionBbQueries(Database):
    """This class handles database transactions for the question"""

    def __init__(self):
        Database.__init__(self, app.config['DATABASE_URL'])

    def insert_question_data(self, data, posted_by):
        """Insert a new question record to the database"""
        query = "INSERT INTO questions (title, description1, date, posted_by)\
        VALUES('{}', '{}', '{}', '{}');".format(data['title'],
                                                data['description1'],
                                                data['date'], posted_by)
        self.cur.execute(query)
        self.conn.commit()

    def fetch_all(self):
        """ Fetches all question records from the database"""
        self.cur.execute("SELECT * FROM questions ")
        rows = self.cur.fetchall()
        questions = []
        for row in rows:
            row = {'id': row[0], 'title': row[1],
                   'description1': row[2],
                   'date': row[3], "posted_by": row[4]
                   }
            questions.append(row)
        return questions
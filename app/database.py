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
        text, date_time timestamp DEFAULT CURRENT_TIMESTAMP, qauthor text)"
        self.cur.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS answers\
        (id SERIAL PRIMARY KEY,aauthor text ,question_id INTEGER, status text,text1 text)"
        self.cur.execute(create_table)
        self.conn.commit()
        self.conn.close()

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

    def fetch_by_paramss(self, table_name, column, param):
        """Fetches a single a parameter from a specific table and column"""
        query = "DELETE FROM {} WHERE {} = '{}'".format(
            table_name, column, param)
        self.cur.execute(query)
        row = self.cur.rowcount
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

    def insert_question_data(self, data, qauthor):
        """Insert a new question record to the database"""
        query = "INSERT INTO questions (title, description1, qauthor)\
        VALUES('{}', '{}', '{}');".format(data['title'],
                                          data['description1'],
                                          qauthor)
        self.cur.execute(query)
        self.conn.commit()

    def fetch_all(self):
        """ Fetches all question recods from the database"""
        self.cur.execute("SELECT * FROM questions ")
        rows = self.cur.fetchall()
        questions = []
        for row in rows:
            row = {'id': row[0], 'title': row[1],
                   'description1': row[2],
                   'date_time': row[3], "qauthor": row[4]
                   }
            questions.append(row)
        return questions


class AnswerBbQueries(Database):
    """This class handles database transactions for answers"""

    def __init__(self):
        Database.__init__(self, app.config['DATABASE_URL'])
        self.status = 'answered'

    def post_answer(self, question_id, data, aauthor):
        query = "INSERT INTO answers (aauthor,question_id, status,text1)\
            VALUES('{}','{}', '{}','{}');".format(aauthor, question_id, self.status, data['text1'])
        self.cur.execute(query)
        self.conn.commit()

    def fetch_by_id(self, question_id):
        """ Gets a question by id from the answers table"""
        self.cur.execute(
            "SELECT * FROM answers WHERE question_id = '{}'".format(question_id))
        rows = self.cur.fetchall()
        answers = []
        for row in rows:
            row = {'id': row[0], 'question_id': row[1],
                   'status': row[2], 'text1': row[3], 'aauthor': row[4]
                   }
            answers.append(row)
        return answers

    def update_answer_status(self, question_id, data):
        '''Updates the status in the database'''
        self.cur.execute("UPDATE answers SET status='{}' WHERE id='{}'"
                         .format(data['status'], question_id))
        self.conn.commit()

    def update_answer(self, answer_id, text1):
        self.cur.execute("UPDATE answers SET text1='{}' WHERE id={}"
                         .format(text1, answer_id))
        self.conn.commit()

    def fetch_by_arg(self, colomn, aauthor):
        """ Gets a question by aauthor from the answers table"""
        self.cur.execute(
            "SELECT * FROM answers WHERE {} = '{}'"
            .format(colomn, aauthor))
        rows = self.cur.fetchall()

        answers = []
        for row in rows:
            row = {'id': row[0], 'question_id': row[1],
                   'status': row[2], 'text1': row[3], 'aauthor': row[3]
                   }
            answers.append(row)
        return answers

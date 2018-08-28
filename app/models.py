"""This module handles database queries"""


class User:
    """This class does all database related stuff for the user"""

    def __init__(self, user_id, name, username, password):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password


class Question:
    '''  Defines a Question class'''

    def __init__(self, question_id, title, description1, date_time, posted_by):
        ''' Initializes the question object'''
        self.question_id = question_id
        self.title = title
        self.description1 = description1
        self.date_time = date_time
        self.posted_by = posted_by



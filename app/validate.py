"""This module contain functions that handle input validation"""
import re


def validate_user(data):
    """validates the user and return appropriate message"""
    try:
        if not data["name"].strip() or not data["username"].strip()\
                or not data["password"].strip():
            return "all fields are required"

        elif not re.match("^[a-zA-Z_ ]*$", data["name"].strip()) or\
                not re.match("^[a-zA-Z0-9_]*$", data["username"].strip()) or\
                not re.match("^[a-zA-Z0-9_@]*$", data["password"].strip()):
            return "Inputs should only contain alphanemeric characters"
        else:
            return "valid"
    except KeyError:
        return "All keys are required"


def validate_login(data):
    """validates the user and return an appropriate message"""
    try:
        if not data["username"].strip() or not data["password"].strip():
            return "all fields are required"
        elif not re.match("^[a-zA-Z0-9_]*$", data["username"].strip()) and\
                not re.match("^[a-zA-Z0-9_@]*$", data["password"].strip()):
            return "Inputs should only contain alphanemeric characters"
        else:
            return "valid"
    except KeyError:
        return "All keys are required"


def validate_question(data):
    """validates the questions inputs and return appropriate message"""
    try:
        if not data["title"].strip() or not data["description1"].strip():
            return "all fields are required"
        elif not re.match("^[a-zA-Z0-9_ ]*$", data["title"].strip()) or\
                not re.match("^[a-zA-Z0-9_ ]*$", data["description1"].strip()):
            return "questions should only contain alphanemeric characters "
        else:
            return "valid"
    except KeyError:
        return "All keys are required"

def validate_answer(data):
    """validates the questions inputs and return appropriate message"""
    try:
        if not data["text1"].strip():
            return "all fields are required"
        elif not re.match("^[a-zA-Z0-9_ ]*$", data["text1"].strip()) :
            return "answers should only contain alphanemeric characters "
        else:
            return "valid"
    except KeyError:
        return "All keys are required"


[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f32c3979a1e641e78ee872c82104579f)](https://www.codacy.com/app/Toskgreg/StackOverflow-Lite-API2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Toskgreg/StackOverflow-Lite-API2&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/Toskgreg/StackOverflow-Lite-API2.png?branch=develop)](https://travis-ci.org/Toskgreg/StackOverflow-Lite-API2)
[![Coverage Status](https://coveralls.io/repos/github/Toskgreg/StackOverflow-Lite-API2/badge.png?branch=develop)](https://coveralls.io/github/Toskgreg/StackOverflow-Lite-API2?branch=develop)
# StackOverflow-lite
StackOverflow-lite is a question and answer application that provides users with the ability to ask questions and have other users answer the questions

## DESCRIPTION

Stackoverflow-lite is a platform where people can ask questions and provide answers

## Link to Stackoverflow-lite on Github Pages

[Stackoverflow-lite](https://toskgreg.github.io/StackOverflow-lite/)

## Link to Stackoverflow-lite API hosted on heroku

[StackOverflow-Lite_api](https://stackoverflowgreg.herokuapp.com)

### Tools

* Text editor where we write our project files. (VScode)
* Python
* Flask Python Framework -Server-side framework
* Pytest - a Python Testing Framework
* Pylint - a Python linting library 
* Postman -Application to test and consume endpoints
* PEP8 - Style guide

## Routes captured by Stackoverflow-lite

 REQUEST | ROUTE | FUNCTIONALITY
 ------- | ----- | -------------
 POST | /api/v1/auth/signup | Registers a user
 POST | /api/v1/auth/login | Logins a registered user
 GET | /api/v1/questions/ | Fetches all questions
 POST | /api/v1/questions/ | Posts a question
 GET | /api/v1/questions/< questionId> | Fetches a specific question
 POST | /api/v1/Delete/questions/< questionId> | Deletes a specific question
 POST | /api/v1/questions/< question_id>/answer/ | Post an answer to a question
 PUT | /api/v1/questions/< question_id>/answer/< answer_id>/ | Mark an answer as accepted or update answer
 POST | /api/v1/questions/< question_id>/< answer_id>/comment | Post a comment to answer
 POST | /api/v1/questions/< question_id>/< answer_id>/upvote | Upvote answer
 POST | /api/v1/questions/< question_id>/< answer_id>/downvote | Downvote  answer


## BUIT WITH

 * Flask-Python

## HOW TO RUN THE APPLICATION

 ### SETING UP THE ENVIRONMENT
 
 1. Clone this repository to your local PC

    ` git clone https://github.com/Toskgreg/StackOverflow-Lite-API2.git `

 2. Create a virtual environment to run application specific dependencies

    ` $ virtualenv venv `
    ` $ source venv/bin/activate `
    ` $ pip install flask `

 ### RUN THE APP

 1. To run the app

    ` python run.py `

 2. To run tests
    `  nosetests --with-coverage --cover-package=app && coverage report `
## Author

**Toskin Gregory**

## Credits
 To Ruganda Mubarak for his insiteful use of tools that have helped me understand this challenge.


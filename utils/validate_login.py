from flask import session
from models import people


def valid_login(username, password):
    # TODO Implement
    return username and password


def log_the_user_in(username):
    # TODO change to user id once things are implemented
    session['username'] = username
    return "Welcome, {}".format(username)


def is_logged_in():
    return 'username' in session


def create_user(username, password):
    user = people.User(
        name=username,
    )
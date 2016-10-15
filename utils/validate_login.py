from flask import session


def valid_login(username, password):
    # TODO Implement
    return username and password

def log_the_user_in(username):
    # TODO change to user id once things are implemented
    session['username'] = username
    return "Welcome, {}".format(username)
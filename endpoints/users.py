import os

from flask import request, render_template, redirect, url_for, flash, session, jsonify

from flask_login import login_required, logout_user, login_user

from requests_oauthlib import OAuth2Session

from endpoints.utils import root
from utils.validate_login import register_user, check_user_exists
from utils import errors

client_id = os.environ['SOCIAL_AUTH_SLACK_KEY']
client_secret = os.environ['SOCIAL_AUTH_SLACK_SECRET']
authorization_base_url = 'https://slack.com/oauth/authorize'
access_token_url='https://slack.com/api/oauth.access'
scope = ['identify']


@root.route('/login', methods=['POST', 'GET'])
def login():
    slack = OAuth2Session(client_id, scope=scope)
    authorization_url, state = slack.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@root.route('/slack-authorized')
def oauth_success():
    slack = OAuth2Session(client_id, state=session['oauth_state'])
    token = slack.fetch_token(access_token_url, client_secret=client_secret,
                               authorization_response=request.url)
    req = slack.get('https://slack.com/api/auth.test?token={}'.format(token['access_token']))

    resp = req.json()

    if resp['team'] != 'Hack Western 3':
        raise errors.InvalidUsage("Expected Hack Western 3 team. Got {}".format(resp['team']))

    person = check_user_exists(resp['user_id'])

    # No person in db. Register.
    if not person:
        session['new_user'] = resp
        return redirect(url_for('register'))

    # Login successful! Show dashboard.
    return redirect('/')


@root.route('/register', methods=['GET', 'POST'])
def register():
    new_user = session.get('new_user')

    # No user to be registered
    if not new_user:
        return redirect('/')

    if request.method == 'GET':
        return render_template("skill.html")
    else:
        incoming_data = request.json()
        register_user(
            {'skill': incoming_data['skill']},
            incoming_data.get('team_data'),
        )
        return redirect('/')


@root.route('/logout', methods=['GET'])
def logout():
    """Logout view"""
    logout_user()
    return redirect('/')
from flask import render_template, flash, redirect, url_for, request, abort
from app import app
from app.forms import LoginForm
from app.models import User
from werkzeug.urls import url_parse
from app.auth import make_auth_url, check_state, get_tokens, open_auth_url
import sys


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', user=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        auth_url = make_auth_url()
        open_auth_url(auth_url)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/callback')
def callback():
    state = request.args.get('state', '')
    if not check_state(state):
        abort(403)
    tokens = get_tokens(request.args.get('code'))
    print(tokens['access_token'] + '??????' + tokens['refresh_token'], file=sys.stderr)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    #logout_user()
    return redirect(url_for('index'))

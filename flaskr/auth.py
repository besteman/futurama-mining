import functools
import logging

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.extensions import db

from flaskr.extensions import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    users = User.query.all()

    logging.info(f'Users: {users}')

    if len(users) == 0:
        stephen_user = User(username='stephen', password=generate_password_hash('1234'))
        besteman_user = User(username='besteman', password=generate_password_hash('123'))
        db.session.add(stephen_user)
        db.session.add(besteman_user)
        db.session.commit()

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        logging.info(f'Logging in for: {username}')
        user = User.query.filter_by(username=username).first()

        if user is None:
            logging.info(f'Username not right for {user}')
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            logging.info(f'Password not right for {user}')
            error = 'Incorrect password.'
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id
        logging.info(f'Setting global user as {g.user}')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

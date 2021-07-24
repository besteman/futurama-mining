import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.extensions import db

from flaskr.extensions import User
from flaskr import app

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    users = User.query.all()

    app.logger(f'Users: {user}')

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
        app.logger(f'Logging in for: {username}')
        user = User.query.filter_by(username=username).first()

        if user is None:
            app.logger(f'Username not right for {user}')
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            app.logger(f'Password not right for {user}')
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
        app.logger(f'Setting global user as {g.user} and id {g.user.id}')
        g.user = User.query.get(user_id)


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

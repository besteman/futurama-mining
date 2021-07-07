from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask.cli import with_appcontext
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from sqlite3 import IntegrityError


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    temp = get_enabled_miners_from_db()
    print(temp)
    db = get_db()
    miners = db.execute(
        'SELECT id, name, enabled, created_at'
        ' FROM miner'
    ).fetchall()
    return render_template('miner/index.html', miners=miners)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        enabled = request.form['enabled']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()

            try:
                db.execute(
                    'INSERT INTO miner (name, enabled)'
                    ' VALUES (?, ?)',
                    (name, enabled)
                )
                db.commit()
            except IntegrityError as err:
                db.rollback()
                return render_template('miner/dup_name.html')
            return redirect(url_for('index.index'))

    return render_template('miner/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    miner = get_miner(id)

    if request.method == 'POST':
        name = request.form['name']
        enabled = request.form['enabled']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE miner SET name = ?, enabled = ?'
                ' WHERE id = ?',
                (name, enabled, id)
            )
            db.commit()
            return redirect(url_for('index.index'))

    return render_template('miner/update.html', miner=miner)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_miner(id)
    db = get_db()
    db.execute('DELETE FROM miner WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index.index'))


def get_miner(id, check_author=True):
    miner = get_db().execute(
        'SELECT m.id, name, enabled, created_at'
        ' FROM miner m'
        ' WHERE m.id = ?',
        (id,)
    ).fetchone()

    if miner is None:
        abort(404, f"Post id {id} doesn't exist.")

    return miner

@with_appcontext
def get_enabled_miners_from_db():
    db = get_db()

    enabled_miners = []

    enabled_miners_from_db = db.execute(
        'SELECT name, enabled'
        ' FROM miner where enabled = 1'
    ).fetchall()

    for miner in enabled_miners_from_db:
        print(miner['name'])
        print(miner['enabled'])
        enabled_miners.append(miner['name'])

    return enabled_miners

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
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
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO miner (name, enabled)'
                ' VALUES (?, ?)',
                (name, enabled)
            )
            db.commit()
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
            error = 'Title is required.'

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
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from sqlite3 import IntegrityError
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.extensions import db, Miner

bp = Blueprint('index', __name__)


@bp.route('/')
def index():

    miners = Miner.query.all()

    current_app.logger.info(f'Miners found: {miners}')

    return render_template('miner/index.html', miners=miners)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    current_app.logger.info('Starting create route')
    if request.method == 'POST':
        name = request.form['name']
        user_enabled = request.form['enabled']
        error = None

        if user_enabled == 'True':
            enabled = True
        else:
            enabled = False

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:

            try:
                current_app.logger.info(f'Creating miner: {name}, {enabled}, {g.user}')
                user_created_miner = Miner(name=name, enabled=enabled, created_user_id=g.user)

                db.session.add(user_created_miner)
                db.session.commit()

                current_app.logger.info(f'Created miner: {name}, {enabled}, {g.user}')
            except IntegrityError as err:
                db.session.rollback()
                return render_template('miner/dup_name.html', err=err)
            except Exception as err:
                db.session.rollback()
                current_app.logger.error(f'Erroring creating miner: {name}, {enabled}, {g.user}, {err}')
            return redirect(url_for('index.index'))

    return render_template('miner/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    miner = get_miner(id)

    if request.method == 'POST':
        name = request.form['name']
        user_enabled = request.form['enabled']
        error = None

        if user_enabled == 'True':
            enabled = True
        else:
            enabled = False

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            current_app.logger.info(f'Updating miner: {name}, {enabled}, {id}')

            miner.name = name
            miner.enabled = enabled

            db.session.commit()

            current_app.logger.info(f'Updated miner: {name}, {enabled}, {id}')
            return redirect(url_for('index.index'))

    return render_template('miner/update.html', miner=miner)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    miner = get_miner(id)

    current_app.logger.info(f'Deleting miner: {miner.name}, {miner.enabled}, {id}')

    db.session.delete(miner)
    db.session.commit()

    current_app.logger.info(f'Deleted miner: {miner.name}, {miner.enabled}, {id}')
    return redirect(url_for('index.index'))


def get_miner(id, check_author=True):
    miner = Miner.query.get(id)

    current_app.logger.info(f'Found miner for get_miner with {id}: {miner}')

    if miner is None:
        abort(404, f"Post id {id} doesn't exist.")

    return miner

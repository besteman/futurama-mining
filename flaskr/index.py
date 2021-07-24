import logging

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask.cli import with_appcontext
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from sqlite3 import IntegrityError

from apscheduler.schedulers.blocking import BlockingScheduler

from flaskr.alerts import main
from flaskr.extensions import db, Miner, User

bp = Blueprint('index', __name__)


@bp.route('/')
def index():


    # # Create an instance of scheduler and add function.
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main, "interval", seconds=10)

    # scheduler.start()
    miners = Miner.query.all()

    logging.info(f'Miners found: {miners}')

    return render_template('miner/index.html', miners=miners)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():

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
                logging.info(f'Creating miner: {name}, {enabled}, {g.user}')
                user_created_miner = Miner(name=name, enabled=enabled, created_user_id=g.user.id)
                db.session.add(user_created_miner)
                db.session.commit()
                logging.info(f'Created miner: {name}, {enabled}, {g.user}')
            except IntegrityError as err:
                db.session.rollback()
                return render_template('miner/dup_name.html')
            except Exception as err:
                logging.info(f'Created miner: {name}, {enabled}, {g.user}')
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
            logging.info(f'Updating miner: {name}, {enabled}, {id}')
            miner.name = name
            miner.enabled = enabled
            db.session.commit()
            logging.info(f'Updated miner: {name}, {enabled}, {id}')
            return redirect(url_for('index.index'))

    return render_template('miner/update.html', miner=miner)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    miner = get_miner(id)
    logging.info(f'Deleting miner: {name}, {enabled}, {id}')
    db.session.delete(miner)
    db.session.commit()
    logging.info(f'Deleted miner: {name}, {enabled}, {id}')
    return redirect(url_for('index.index'))


def get_miner(id, check_author=True):
    miner = Miner.query.get(id)
    logging.info(f'Found miner for get_miner with {id}: {miner}')
    if miner is None:
        abort(404, f"Post id {id} doesn't exist.")

    return miner



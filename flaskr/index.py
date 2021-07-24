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

    if len(miners) == 0:
        planet_express = Miner(name='planet_express', enabled=True, created_user_id=1)
        nimbus = Miner(name='nimbus', enabled=False, created_user_id=1)
        db.session.add(planet_express)
        db.session.add(nimbus)
        db.session.commit()
        miners = Miner.query.all()

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
                user_created_miner = Miner(name=name, enabled=enabled, created_user_id=g.user.id)
                db.session.add(user_created_miner)
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                return render_template('miner/dup_name.html')
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
            miner.name = name
            miner.enabled = enabled
            db.session.commit()
            return redirect(url_for('index.index'))

    return render_template('miner/update.html', miner=miner)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    miner = get_miner(id)
    db.session.delete(miner)
    db.session.commit()
    return redirect(url_for('index.index'))


def get_miner(id, check_author=True):
    miner = Miner.query.get(id)

    if miner is None:
        abort(404, f"Post id {id} doesn't exist.")

    return miner



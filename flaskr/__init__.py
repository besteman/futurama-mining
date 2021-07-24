import os

from flask import Flask
from flaskr.extensions import db, User, Miner


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # if __name__ == "__main__":
    #     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.app_context().push()
    with app.app_context():
        db.create_all()

    from . import auth
    app.register_blueprint(auth.bp)

    from . import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    return app

app = create_app()
app.app_context().push()
# from flaskr.extensions import User, Miner
# db.create_all()
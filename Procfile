clock: python flaskr/cronjob.py
web: export FLASK_APP=flaskr && export FLASK_ENV=production && flask init-db && gunicorn "flaskr:create_app()"
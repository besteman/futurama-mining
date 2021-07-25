# futurama-mining

## Setup Alerts

### Virtual Env

* Install Package for Envs

```sh
python3 -m pip install --user virtualenv
```

* Create virtual environment

```sh
python3 -m venv futurama-mining-env
```

* Activate virtual environment

```sh
. futurama-mining-env/bin/activate
```

* Upgarde Pip

```sh
pip install --upgrade pip
```

* Install packages to environment

```sh
pip install -r requirements.txt
```

> Note: You have to do this every time you add a package, remove a package, and upgrade package

* Leave environment

```sh
deactivate
```

### Docker

**TODO update this to work with PostgreSQL**

To run alerts, you need to download and [install docker](https://docs.docker.com/get-docker/).

You will also need to get `.env` file that stores creds for login into Gmail server.

Once you have downloaded docker you can run:

`docker build --tag alerts .`

And to run the docker container:

`docker run alerts`

## Run Miner Web App

> Note, you have to be in the virtual env!

### Packages

All packages should be included in the requirements.txt file.

### Set Bash Variables

```sh
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
flask run
```

The miner app should now be running on `http://127.0.0.1:5000/` and has hot reloading

## Prod

Everything is running on Heroku

### Database

#### Dev

On dev, miner app will use SQLite to mimic prod's database

#### Prod

Prod is running on Heroku PostgreSQL Addon. Everything should be automatic in terms of setup and connection

#### Migrations

Migrations are handled through [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/), which is a wrapper for [Alembic](https://alembic.sqlalchemy.org/en/latest/)

All migrations are stored in [version folder](migrations/versions)

If you update a SQLAlchemy class, add column, change column size, delete column, etc, flask-migrate should be able to detect that change with the following:

```sh
flask db migrate -m "MIGRATIONS MESSAGE"
```

This will create a migration file in the [version folder](migrations/versions). When you deploy to Heroku, the migration will run automatically for you.
# futurama-mining

## Run Alerts

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
source futurama-mining-env/bin/activate
```

* Install packages to environment

```sh
python3 -m pip install -r requirements.txt
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

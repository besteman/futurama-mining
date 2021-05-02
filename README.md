# futurama-mining

## Run Alerts

To run alerts, you need to download and [install docker](https://docs.docker.com/get-docker/). 

You will also need to get `.env` file that stores creds for login into Gmail server.

Once you have downloaded docker you can run:

`docker build --tag alerts .`

And to run the docker container:

`docker run alerts`

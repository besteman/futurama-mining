import os
# import smtplib

import logging
from dotenv import load_dotenv
import requests
from twilio.rest import Client

from flaskr.extensions import db, Miner

from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()

# ACCOUNT_SID = os.environ['account_sid'] or None
# AUTH_TOKEN = os.environ['auth_token'] or None

# GMAIL_ADDRESS: str = os.environ['gmail_address']
# GMAIL_PW: str = os.environ['gmail_pw']

BASE_ETH_URL: str = 'https://api.nanopool.org/v1/eth/'
ETH_MINER_ADDRESS: str = '0x5d78c71912ea88c23c602c8e0d5363d1e3cba4be'
PHONE_NUMBERS: list = [os.environ.get('besteman_number'), os.environ.get('stephen_number')]

schedule = BlockingScheduler()


def get_enabled_miners_from_db():

    enabled_miners_from_db = Miner.query.filter_by(enabled=True).all()

    logging.info(f'Miners found DB: {enabled_miners_from_db}')

    enabled_miners = []
    for miner in enabled_miners_from_db:
        enabled_miners.append(enabled_miners_from_db.name)

    logging.info(f'enabled_miners are: {enabled_miners}')

    return enabled_miners


def get_workers_reported_hashrate() -> dict:
    """Hits Nanopool API to get last reported hashrates

    Returns:
        dict: A dict of workers and their hashrates
    """
    response = requests.get(f'{BASE_ETH_URL}reportedhashrates/{ETH_MINER_ADDRESS}')
    response: dict = response.json()

    return response['data']


def check_workers_hashrate(workers_hashrate: dict) -> list:
    """Check if any workers' hashrate is at 0, if hashrate is at 0 it will all to list and return

    Args:
        workers_hashrate (dict): Workers and their hashrates

    Returns:
        list: list of workers that hashrate is equal 0
    """
    offline_workers: list = []

    enabled_miners: list = get_enabled_miners_from_db()
    enabled_miners = []
    for worker in workers_hashrate:
        if worker['hashrate'] == 0 and worker['worker'] not in enabled_miners:
            offline_workers.append(worker['worker'])

    return offline_workers


def send_text_message(offline_workers: list) -> None:
    """If any workers' hashrate is equal to zero, this function will be called and send a text message

    Args:
    offline_workers (list): Workers that hashrate is equal to zero
    """
    txt_body: str = f"""Panic! At the Hashrate! \n{', '.join(offline_workers)} rigs are reporting 0 hashrate"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for phone_number in PHONE_NUMBERS:
        client.api.account.messages.create(
            to=phone_number,
            from_=os.environ.get('twilio_number'),
            body=txt_body)

@schedule.scheduled_job('interval', seconds=10)
def main():
    """Main function that start the process
    """
    logging.info("Starting Cronjob")

    workers_hashrate: dict = get_workers_reported_hashrate()

    logging.info(f'Workers hashrates {workers_hashrate}')

    offline_workers: list = check_workers_hashrate(workers_hashrate)

    logging.info(f'Offline Workers: {offline_workers}')

    # if offline_workers:
    #     send_text_message(offline_workers)
    # else:
    #     print('No Workers are at 0')

schedule.start()
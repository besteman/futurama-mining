import json
import os

from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv('account_sid')
AUTH_TOKEN = os.getenv('auth_token')

BASE_ETH_URL = 'https://api.nanopool.org/v1/eth/'
ETH_MINER_ADDRESS = '0x5d78c71912ea88c23c602c8e0d5363d1e3cba4be'
BASE_LIMIT = 950
PHONE_NUMBERS = ['+19413570978', '+19896074589']


def get_workers_reported_hashrate():
    # https://api.nanopool.org/v1/eth/hashrate/:address
    # response = requests.get(BASE_ETH_URL + ETH_MINER_ADDRESS)
    response = requests.get(f'{BASE_ETH_URL}reportedhashrates/{ETH_MINER_ADDRESS}')
    response = response.json()

    return response['data']


def check_workers_hashrate(workers_hashrate):
    offline_workers = []

    for worker in workers_hashrate:
        if worker['hashrate'] == 0:
            offline_workers.append(worker['worker'])

    return offline_workers


def send_txt_msg(offline_workers):
    txt_body = f"""Panic! At the Hashrate! \n{', '.join(offline_workers)} rigs are reporting 0 hashrate"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for phone_number in PHONE_NUMBERS:

        client.api.account.messages.create(
            to=phone_number,
            from_="+12132925602",
            body=txt_body)


def main():
    print("Starting")

    workers_hashrate = get_workers_reported_hashrate()

    print(workers_hashrate)

    offline_workers = check_workers_hashrate(workers_hashrate)

    print(offline_workers)

    if offline_workers:
        send_txt_msg(offline_workers)
    else:
        print(f'No Workers are not below the {BASE_LIMIT}')


if __name__ == "__main__":
    main()
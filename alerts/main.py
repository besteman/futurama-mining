import json
import os

from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')

BASE_ETH_URL = 'https://api.nanopool.org/v1/eth/'
ETH_MINER_ADDRESS = '0x5d78c71912ea88c23c602c8e0d5363d1e3cba4be'
BASE_LIMIT = 950


def get_miner_reported_hashrate():
    # https://api.nanopool.org/v1/eth/hashrate/:address
    # response = requests.get(BASE_ETH_URL + ETH_MINER_ADDRESS)
    response = requests.get(f'{BASE_ETH_URL}reportedhashrate/{ETH_MINER_ADDRESS}')
    response = response.json()

    return response['data']


def send_txt_msg():
    # client = Client(account_sid, auth_token)

    # client.api.account.messages.create(
    #     to="+19413570978",
    #     from_="+12132925602",
    #     body="Hello World!")


def main():
    print("Starting")

    reported_hashrate = get_miner_reported_hashrate()

    print(reported_hashrate)

    if reported_hashrate < BASE_LIMIT:
        send_txt_msg()
    else:
        print(f'Reported hashrate is not below the {BASE_LIMIT}')




# client = Client(account_sid, auth_token)

# client.api.account.messages.create(
#     to="+19413570978",
#     from_="+12132925602",
#     body="Hello World!")

if __name__ == "__main__":
    main()
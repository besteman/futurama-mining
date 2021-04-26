import json
import os

from dotenv import load_dotenv
import requests
import smtplib
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv('account_sid')
AUTH_TOKEN = os.getenv('auth_token')
GMAIL_ADDRESS = os.getenv('gmail_address')
GMAIL_PW = os.getenv('gmail_pw')

BASE_ETH_URL = 'https://api.nanopool.org/v1/eth/'
ETH_MINER_ADDRESS = '0x5d78c71912ea88c23c602c8e0d5363d1e3cba4be'
EMAIL_ADDRESS = ['9413570978@vtext.com']


def get_workers_reported_hashrate():
    response = requests.get(f'{BASE_ETH_URL}reportedhashrates/{ETH_MINER_ADDRESS}')
    response = response.json()

    return response['data']


def check_workers_hashrate(workers_hashrate):
    offline_workers = []

    for worker in workers_hashrate:
        if worker['hashrate'] == 0:
            offline_workers.append(worker['worker'])

    return offline_workers


def send_email(offline_workers):
    email_body = f"""Panic! At the Hashrate! \n{', '.join(offline_workers)} rigs are reporting 0 hashrate"""

    try:
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(GMAIL_ADDRESS, GMAIL_PW)

        subject = 'Panic! At the Hashrate!'
        body = f'{", ".join(offline_workers)} rigs are reporting 0 hashrate'

        message = f'Subject: {subject}\n\n{body}'
        server.sendmail(GMAIL_ADDRESS, EMAIL_ADDRESS, email_body)
        server.quit()
    except Exception as e:
        print(f'Something went wrong... {e}')


def main():
    print("Starting")

    workers_hashrate = get_workers_reported_hashrate()

    print(workers_hashrate)

    offline_workers = check_workers_hashrate(workers_hashrate)

    print(offline_workers)

    if offline_workers:
        send_email(offline_workers)
    else:
        print(f'No Workers are not at 0')


if __name__ == "__main__":
    main()
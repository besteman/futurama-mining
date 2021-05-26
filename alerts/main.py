import os
# import smtplib

from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.environ['account_sid']
AUTH_TOKEN = os.environ['auth_token']

# GMAIL_ADDRESS: str = os.environ['gmail_address']
# GMAIL_PW: str = os.environ['gmail_pw']

BASE_ETH_URL: str = 'https://api.nanopool.org/v1/eth/'
ETH_MINER_ADDRESS: str = '0x5d78c71912ea88c23c602c8e0d5363d1e3cba4be'
PHONE_NUMBERS: list = ['+19413570978', '+19896074589']

BLACKLIST = ['best_3070', '3080_is_better', 'quartz_3070', 'Hedonismbot', 'Mr_Peppy']


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

    for worker in workers_hashrate:
        if worker['hashrate'] == 0 and worker['worker'] not in BLACKLIST:
            offline_workers.append(worker['worker'])

    return offline_workers


def send_email(offline_workers: list) -> None:
    """If any workers' hashrate is equal to zero, this function will be called and send any email

    Args:
    offline_workers (list): Workers that hashrate is equal to zero
    """
    txt_body: str = f"""Panic! At the Hashrate! \n{', '.join(offline_workers)} rigs are reporting 0 hashrate"""

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for phone_number in PHONE_NUMBERS:
        client.api.account.messages.create(
            to=phone_number,
            from_="+12132925602",
            body=txt_body)

    # try:
    #     server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    #     server.ehlo()
    #     server.starttls()
    #     server.login(GMAIL_ADDRESS, GMAIL_PW)

    #     server.sendmail(GMAIL_ADDRESS, EMAIL_ADDRESS, email_body)
    #     server.quit()
    # except Exception as e:
    #     print(f'Something went wrong... {e}')


def main():
    """Main function that start the process
    """
    print("Starting")

    workers_hashrate: dict = get_workers_reported_hashrate()

    print(workers_hashrate)

    offline_workers: list = check_workers_hashrate(workers_hashrate)

    print(offline_workers)

    if offline_workers:
        send_email(offline_workers)
    else:
        print('No Workers are at 0')


if __name__ == "__main__":
    main()

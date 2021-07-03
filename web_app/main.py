from flask import Flask
from flask import request
import json

app = Flask(__name__)


def read_in_miner_data():
    with open('web_app/data/miners.json') as data:
        temp_data = json.load(data)
        return temp_data


def check_if_miner_exists(miner_data, miner_name):
    for data in miner_data:
        print(data)
        if miner_name in data['miner']:
            return True

    return False


def write_new_miner_to_data(miner_data, miner_name, enabled=True):
    new_dict_miner = {
        'miner': miner_name,
        'enabled': enabled
    }
    miner_data.append(new_dict_miner)
    with open('web_app/data/miners.json', 'w') as file:
        json.dump(miner_data, file)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# @app.route("/add-miner/", methods=['POST'])
def add_miner():

    # print(request.form['miner-name'])

    new_miner = 'that'

    miner_data = read_in_miner_data()

    print(miner_data)

    miner_exist = check_if_miner_exists(miner_data, new_miner)

    print(miner_exist)

    if miner_exist is True:
        return '<p>Miner Already Exists</p>'

    write_new_miner_to_data(miner_data, new_miner, enabled=False)

    return "<p>Hello, World!</p>"


add_miner()

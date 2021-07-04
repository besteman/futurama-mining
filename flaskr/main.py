from flask import Flask
from flask import request
import json

app = Flask(__name__)


def read_in_miner_data():
    with open('data/miners.json') as data:
        temp_data = json.load(data)
        return temp_data


def check_if_miner_exists(miner_data, miner_name):
    for data in miner_data:
        print(data)
        if miner_name in data['miner']:
            return True

    return False


def write_new_miner_to_data(miner_data, miner_name, enabled=True):
    print('how')
    new_dict_miner = {
        'miner': miner_name,
        'enabled': enabled
    }
    miner_data.append(new_dict_miner)
    print('there')
    with open('data/miners.json', 'w') as file:
        print('loading data')
        json.dump(miner_data, file)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/add-miner/", methods=['POST', 'GET'])
def add_miner():

    if request.form['enabled'] == 'true':
        enabled = True
    else:
        enabled = False

    miner_data = read_in_miner_data()

    print(miner_data)

    miner_exist = check_if_miner_exists(miner_data, request.form['miner-name'])

    print(miner_exist)

    if miner_exist is True:
        return '<p>Miner Already Exists</p>'

    print(request.form)
    write_new_miner_to_data(miner_data, request.form['miner-name'], enabled=enabled)

    return "<p>Miner added!</p>"

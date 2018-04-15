# -*- coding: UTF-8 -*-
import json
import requests
from flask import Flask
from flask import jsonify
from flask import request
from src import blockchain

# Instantiate our Node
app = Flask(__name__)

@app.route('/transactions/new', methods=['GET'])
def new_transaction():
    req_url = 'http://localhost:5000/transactions/new'
    req_data = '''
    {
        'sender': 'd4ee26eee15148ee92c6cd394edd974e',
        'recipient': 'someone-other-address',
        'amount': 5
    }
    '''
    req_json = json.dumps(req_data)
    hd = 'Content-Type: application/json'
    resp = requests.post(url = req_url, json = req_json)
    return 'We will add a new transaction'

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
    # new_transaction()
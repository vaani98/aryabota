import re
from flask import Flask, request, jsonify

from controller import do
from model import CoinSweeper

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route('/coinSweeper', methods=(['POST']))
def coinSweeper():
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        response = do(commands)
        return jsonify(response)

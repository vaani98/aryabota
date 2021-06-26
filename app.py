import re
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from controller import do
from model import CoinSweeper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:3000"}})


@app.route("/")
@cross_origin()
def index():
    return "Hello World!"


@app.route('/coinSweeper', methods=(['POST']))
def coinSweeper():
    print("@@", request)
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        # print("!!", request)
        response = do(commands)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(response)

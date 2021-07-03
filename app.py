import re
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from controller import do
from model import CoinSweeper

app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def index():
    return "Hello World!"


@app.route('/coinSweeper', methods=(['POST', 'OPTIONS']))
@cross_origin()
def coinSweeper():
    print("@@", request)
    if request.method == 'OPTIONS':
        return ("", 200)
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        # print("!!", request)
        response = do(commands)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return jsonify(response)

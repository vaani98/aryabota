"""Flask App"""
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from controller import understand

app = Flask(__name__)
CORS(app)


@app.route("/")
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"


@app.route('/coinSweeper', methods=(['POST', 'OPTIONS']))
@cross_origin()
def coin_sweeper():
    """Execute commands input in pseudo-code"""
    print("@@", request)
    if request.method == 'OPTIONS':
        return ("", 200)
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        response = understand(commands)
        return jsonify(response)
    return ("", 405)

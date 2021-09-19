"""Flask App"""
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import logging

from lexer_parser import understand
from services import user, problem

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, filename="app.log", format="%(levelname)s-%(funcName)s-%(asctime)s: %(message)s")

# Endpoints
@app.route('/')
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"

# User API Endpoint
@app.route('/api/user', methods = ['POST','GET'])
@cross_origin()
def user_endpoint():
    """ Create and Exists operations for User """
    if request.method == 'GET':
        # Checking if user exists
        email = request.args.get('email')
        if user.exists(email):
            return True
    if request.method == 'POST':
        # Storing user survey details
        return user.create(request.json)

# Problem Endpoint
@app.route('/api/problem', methods = ['GET'])
@cross_origin()
def problem_endpoint():
    """ Render specified problem grid """
    if request.method == 'GET':
        # Getting problem grid for the requested level
        level = request.args.get('level')
        return jsonify(problem.render(level))
    if request.method == 'POST':
        level = request.json['level']
        problem.render(level)
        user_email = request.json['email']
        commands = request.json['commands']
        logging.info(f'User email {user_email}, received commands to execute:\n{commands}')
        response = understand(commands)
        return jsonify(response)

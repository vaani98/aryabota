"""Flask App"""
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import yaml
from jsonschema import RefResolver, Draft7Validator

from grid import Grid
from coin_sweeper import CoinSweeper
from problem import Problem
from lexer_parser import understand
from utils import get_for_every_position

"""Opening config to read grid attributes"""
with open('../config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
app = Flask(__name__)
CORS(app)


"""Utils"""
"""Build the JSON Schema and Store for Resolver and Draft7Validator"""
def build_schema_and_store():
    schema_file = open("../resources/schema/problem.json")
    schema = json.loads(schema_file.read())
    state_schema_file = open("../resources/schema/problem_state.json")
    state_schema = json.loads(state_schema_file.read())
    position_schema_file = open("../resources/schema/position.json")
    position_schema = json.loads(position_schema_file.read())
    schema_store = {
        schema['$id'] : schema,
        state_schema['$id'] : state_schema,
        position_schema['$id'] : position_schema
    }
    return schema, schema_store

"""Validate the input problem file"""
def validate(problem_file_path):
    problem_file = open(problem_file_path)
    problem = json.loads(problem_file.read())
    schema, schema_store = build_schema_and_store()
    resolver = RefResolver.from_schema(schema, store = schema_store)
    validator = Draft7Validator(schema, resolver = resolver)
    validator.validate(problem)
    return problem

"""Initialise the state of the grid"""
def initialise_state(problem):
    problem_details = problem["problem"]
    state = problem["initial_state"]
    bot = CoinSweeper.get_instance()
    coin_sweeper_state = state["coin_sweeper"]
    if "pen" in coin_sweeper_state:
        bot.configure(coin_sweeper_state["position"]["row"], coin_sweeper_state["position"]["column"], coin_sweeper_state["dir"], coin_sweeper_state["pen"])
    else:
        bot.configure(coin_sweeper_state["position"]["row"], coin_sweeper_state["position"]["column"], coin_sweeper_state["dir"], "down")
    grid = Grid.get_instance()
    grid_state = state["grid"]
    rows = grid_state["dimensions"]["row"]
    columns = grid_state["dimensions"]["column"]
    coins_per_position = obstacles_per_position = None
    if "coins" in grid_state:
        coins_per_position = get_for_every_position(grid_state["coins"], rows, columns)
    else:
        grid_state["coins"] = None
    if "obstacles" in grid_state:
        obstacles_per_position = get_for_every_position(grid_state["obstacles"], rows, columns, False)
    else:
        grid_state["obstacles"] = None
    grid.configure(rows, columns, grid_state["coins"], coins_per_position, grid_state["obstacles"], obstacles_per_position)
    problem_instance = Problem.get_instance()
    problem_instance.configure(problem_details["problem_type"], problem_details["statement"], problem["answer"])

@app.before_first_request
def before_first_request():
    """Reading and validating config against schema, initialising the grid"""
    problem_file_path = "../resources/problem-grids/shortest_path.json"
    problem = validate(problem_file_path)
    initialise_state(problem)   

@app.route("/")
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"

@app.route('/reset', methods=(['POST']))
@cross_origin()
def reset():
    """To reset the given problem"""
    before_first_request()
    problem = Problem.get_instance()
    return jsonify(problem.get_initial_state())

@app.route('/coinSweeper', methods=(['POST', 'GET', 'OPTIONS']))
@cross_origin()
def coin_sweeper():
    """Execute commands input in pseudo-code"""
    print("@@", request)
    if request.method == 'OPTIONS':
        return ("", 200)
    if request.method == 'GET':
        problem = Problem.get_instance()
        return jsonify(problem.get_initial_state())
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        response = understand(commands)
        return jsonify(response)
    return ("", 405)

@app.route('/submitAnswer', methods=(['POST']))
@cross_origin()
def submit_answer():
    print("@@", request, request.json)
    submitted_answer = request.json
    problem = Problem.get_instance()
    response = problem.check_answer(submitted_answer)
    return jsonify(response)

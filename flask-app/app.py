"""Flask App"""
import json
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS, cross_origin
import yaml
from jsonschema import RefResolver, Draft7Validator

from grid import Grid
from coin_sweeper import CoinSweeper
from problem import Problem
from lexer_parser import understand
from utils import get_for_every_position

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
    statement = problem_details["statement"]
    problem_spec = problem_details["problem_spec"]
    if "coins" in grid_state:
        coins_per_position = get_for_every_position(grid_state["coins"], rows, columns)
    else:
        grid_state["coins"] = None
    if "obstacles" in grid_state:
        obstacles_per_position = get_for_every_position(grid_state["obstacles"], rows, columns, False)
    else:
        grid_state["obstacles"] = None
    if not "homes" in grid_state:
        grid_state["homes"] = None
    grid.configure(rows, columns, grid_state["coins"], coins_per_position, grid_state["obstacles"], obstacles_per_position, grid_state["homes"], statement, problem_spec)
    problem_instance = Problem.get_instance()
    problem_instance.configure(problem_details["problem_type"], problem_details["statement"], problem["answer"])

def read_config_and_initialise():
    """Opens config, reads current problem grid set and initializes the grid"""
    with open('../config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        problem_file_path = "../" + config["app"]["problem_grid"]
        """Reading and validating config against schema, initialising the grid"""
        problem = validate(problem_file_path)
        initialise_state(problem)
        problem = Problem.get_instance()
        return jsonify(problem.get_initial_state())

@app.route('/set_problem', methods = ['POST'])
@cross_origin()
def set_problem():
    problem = request.json["level"]
    print("Problem = ", problem)
    problems = {
        'count_coins': 'count_number_of_coins.json',
        'go_home': 'go_home.json',
        'check_coins': 'check_and_pick_coins.json',
        'coins_lte': 'coins_lte_30.json',
        'coins_gte': 'coins_gte_10.json',
        'Level_1_Easy':'Level_1_Easy.json',
        'Level_1_Medium':'Level_1_Medium.json',
        'shortest_path': 'shortest_path.json',
        'colour_border': 'colour_boundary.json',
        'colour_alternate': 'colour_alternate.json',
        'colour_coin_locations': 'colour_coin_locations.json',
        'boolean_easy': 'boolean_easy.json'
        }
    problem_file_path = "resources/problem-grids/" + problems[problem]
    """Opening config to read grid attributes"""
    with open('../config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        config["app"]["problem_grid"] = problem_file_path
    with open('../config.yaml', 'w') as f:
        yaml.dump(config, f)
    return read_config_and_initialise()

@app.route('/set_language', methods = ['POST'])
@cross_origin()
def set_language():
    """Opening config to read grid attributes"""
    with open('../config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        language = request.json["lang"].lower()
        print("Language being set is: ", language)
        config["app"]["language"] = language
    with open('../config.yaml', 'w') as f:
        yaml.dump(config, f)
    return read_config_and_initialise()

@app.before_first_request
def before_first_request():
    """Reading and validating config against schema, initialising the grid"""
    return read_config_and_initialise()

@app.route("/")
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"

@app.route('/reset', methods=(['POST']))
@cross_origin()
def reset():
    """To reset the given problem"""
    return read_config_and_initialise()
    

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

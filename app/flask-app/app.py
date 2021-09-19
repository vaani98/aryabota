"""Flask App"""
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import yaml
import logging
from jsonschema import RefResolver, Draft7Validator

from grid import Grid
from coin_sweeper import CoinSweeper
from problem import Problem
from lexer_parser import understand
from utils import get_for_every_position

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG, filename="app.log", format="%(levelname)s-%(funcName)s-%(asctime)s: %(message)s")

# Utils
def build_schema_and_store():
    """Build the JSON Schema and Store for Resolver and Draft7Validator"""
    schema_file = open("resources/schema/problem.json")
    schema = json.loads(schema_file.read())
    state_schema_file = open("resources/schema/problem_state.json")
    state_schema = json.loads(state_schema_file.read())
    position_schema_file = open("resources/schema/position.json")
    position_schema = json.loads(position_schema_file.read())
    schema_store = {
        schema['$id'] : schema,
        state_schema['$id'] : state_schema,
        position_schema['$id'] : position_schema
    }
    return schema, schema_store

def validate(problem_file_path):
    """Validate the input problem file"""
    problem_file = open(problem_file_path)
    problem = json.loads(problem_file.read())
    schema, schema_store = build_schema_and_store()
    resolver = RefResolver.from_schema(schema, store = schema_store)
    validator = Draft7Validator(schema, resolver = resolver)
    validator.validate(problem)
    return problem

def initialise_state(problem):
    """Initialise the state of the grid"""
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
    with open('config.yaml') as req_file:
        config = yaml.load(req_file, Loader=yaml.FullLoader)
        problem_file_path = config["app"]["problem_grid"]
        # Reading and validating config against schema, initialising the grid
        problem = validate(problem_file_path)
        initialise_state(problem)
        problem = Problem.get_instance()
        return jsonify(problem.get_initial_state())

@app.before_first_request
def before_first_request():
    """Reading and validating config against schema, initialising the grid"""
    return read_config_and_initialise()

# Endpoints
@app.route("/")
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"

@app.route('/set_problem', methods = ['POST'])
@cross_origin()
def set_problem():
    """Set Problem API"""
    problem = request.json["level"]
    problems = {
        'go_home': 'L0_P1.json',
        'all_homes': 'L0_P2.json',
        'shortest_path': 'L0_P3.json',
        'Level_1_Easy':'L1_P1.json',
        'Level_1_Medium':'L1_P2.json',
        'colour_border': 'L1.5_P1.json',
        'colour_alternate': 'L1.5_P2.json',
        'check_and_color': 'L1.5_P3.json',
        'check_coins': 'L2_P1.json',
        'coins_gte': 'L2_P2.json',
        'coins_lte': 'L2_P3.json',
        }
    problem_file_path = "resources/problem-grids/" + problems[problem]
    # Opening config to read grid attributes
    with open('config.yaml') as req_file:
        config = yaml.load(req_file, Loader=yaml.FullLoader)
        config["app"]["problem_grid"] = problem_file_path
    with open('config.yaml', 'w') as req_file:
        yaml.dump(config, req_file)
    logging.info(f'Setting problem to {problem}')
    return read_config_and_initialise()

@app.route('/set_language', methods = ['POST'])
@cross_origin()
def set_language():
    """Opening config to read grid attributes"""
    with open('config.yaml') as req_file:
        config = yaml.load(req_file, Loader=yaml.FullLoader)
        language = request.json["lang"].lower()
        config["app"]["language"] = language
    with open('config.yaml', 'w') as req_file:
        yaml.dump(config, req_file)
    logging.info(f'Setting language to {language}')
    return read_config_and_initialise()

@app.route('/reset', methods=(['POST']))
@cross_origin()
def reset():
    """To reset the given problem"""
    logging.info(f'Resetting problem')
    return read_config_and_initialise()

@app.route('/coinSweeper', methods=(['POST', 'GET', 'OPTIONS']))
@cross_origin()
def coin_sweeper():
    """Execute commands input in pseudo-code"""
    if request.method == 'OPTIONS':
        return ("", 200)
    if request.method == 'GET':
        logging.info(f'Getting problem state')
        problem = Problem.get_instance()
        return jsonify(problem.get_initial_state())
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        logging.info(f'Received commands to execute:\n{commands}')
        response = understand(commands)
        return jsonify(response)
    return ("", 405)

@app.route('/submitAnswer', methods=(['POST']))
@cross_origin()
def submit_answer():
    """Submit Answer API"""
    logging.info(f'Answer submitted, checking')
    submitted_answer = request.json
    problem = Problem.get_instance()
    response = problem.check_answer(submitted_answer)
    return jsonify(response)

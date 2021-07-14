"""Flask App"""
import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import yaml

from grid import Grid
from coin_sweeper import CoinSweeper
from lexer_parser import understand, get_initial_state
from utils import lint_problem_grid

"""Opening config to read grid attributes"""
with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
app = Flask(__name__)
CORS(app)

@app.before_first_request
def before_first_request():
    """Reading and linting config, initialising the grid"""
    bot = CoinSweeper.get_instance()
    grid = Grid.get_instance()
    with open("../resources/problem-grids/" + config["app"]["problem_grid"]) as problem_grid_file:
        problem_grid = json.loads(problem_grid_file.read())
        linted_problem_grid = lint_problem_grid(problem_grid)
        if linted_problem_grid:
            grid.configure(linted_problem_grid["rows"], linted_problem_grid["columns"], linted_problem_grid["coins"], linted_problem_grid["coins_per_position"], linted_problem_grid["obstacles"], linted_problem_grid["obstacles_per_position"])
            coin_sweeper_start = linted_problem_grid["coin_sweeper_start"]
            bot.configure(coin_sweeper_start["row"], coin_sweeper_start["column"], coin_sweeper_start["dir"])
        else:
            raise Exception("Couldn't initialise problem grid!")

@app.route("/")
@cross_origin()
def index():
    """Hello World"""
    return "Hello World!"

@app.route('/reset', methods=(['POST']))
@cross_origin()
def reset():
    """To reset the given problem - Yet to add the reset button in UI"""
    before_first_request()
    return "RESET successful"

@app.route('/coinSweeper', methods=(['POST', 'GET', 'OPTIONS']))
@cross_origin()
def coin_sweeper():
    """Execute commands input in pseudo-code"""
    print("@@", request)
    if request.method == 'OPTIONS':
        return ("", 200)
    if request.method == 'GET':
        return jsonify(get_initial_state())
    if request.method == 'POST':
        # getting raw data in JSON format, needs header Content-Type = application/json
        commands = request.json
        response = understand(commands)
        return jsonify(response)
    return ("", 405)

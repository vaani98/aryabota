"""Control Hub that makes changes to the CoinSweeper environment - grid and robot"""
"""Writes outcomes to a result file"""
import yaml
import json

from grid import Grid
from coin_sweeper import CoinSweeper
from problem import Problem

"""Opening config to read grid attributes"""
with open('../config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()
results_file_path = config["app"]["results"]

def make_response(response_type, response):
    if response_type == "value":
        return {
            "value": response
        }
    elif response_type == "state":
        return {
            "stateChanges": [response]
        }
    elif response_type == "error":
        return {
            "error_message": response
        }

def get_my_row():
    return bot.my_row()

def get_my_column():
    return bot.my_column()

def move(steps):
    (success, message) = bot.move(steps)
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
        if success:
            results.append(make_response("state", bot.get_state()))
        else:
            results.append(make_response("error", message))
            # TODO: specific error raising
            raise Exception("Hitting obstacles or falling off the grid ;_;")
    print(results)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def turn(direction = "left"):
    if direction == "left":
        bot.turn_left()
    elif direction == "right":
        bot.turn_right()
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
        results.append(make_response("state", bot.get_state()))
    print(results)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def set_pen(status = "up"):
    bot.set_pen(status)

def get_number_of_coins(row = bot.my_row(), column = bot.my_column()):
    # TODO: change to success and message format as with move, GET should never fail silently
    return grid.get_number_of_coins(bot.my_row(),bot.my_column())

def obstacle(row = bot.my_row(), column = bot.my_column()):
    state = grid.get_state()
    dir = bot.get_dir()
    if dir == "down":
        if bot.my_row()+1 <= grid.rows:
            if({'row': bot.my_row()+1, 'column': bot.my_column()} in state['obstacles']):
                return 1
    elif dir == "up":
        if bot.my_row()-1 > 0:
            if({'row': bot.my_row()-1, 'column': bot.my_column()} in state['obstacles']):
                return 1
    elif dir == "right":
        if bot.my_column()+1 <= grid.columns:
            if({'row': bot.my_row(), 'column': bot.my_column()+1} in state['obstacles']):
                return 1
    elif dir == "left":
        if bot.my_column()-1 > 0:
            if({'row': bot.my_row(), 'column': bot.my_column()-1} in state['obstacles']):
                return 1
    return 0 

def print_value(expr):
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    response = expr
    results.append(make_response("value", response))
    print(results)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def submit(value):
    problem = Problem.get_instance()
    if value is not None:
        response = problem.check_answer(value)
    else:
        coin_sweeper_state = bot.get_state()
        response = problem.check_answer(coin_sweeper_state)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(response))
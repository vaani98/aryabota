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
    elif response_type == "submit":
        return response

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
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def set_pen(status = "up"):
    bot.set_pen(status)

def get_number_of_coins(row = bot.my_row(), column = bot.my_column()):
    # TODO: change to success and message format as with move, GET should never fail silently
    return grid.get_number_of_coins(row,column)

def obstacle(row = bot.my_row(), column = bot.my_column()):
    state = grid.get_state()
    dir = bot.get_dir()
    if dir == "down":
        if row+1 <= grid.rows:
            if({'row': row+1, 'column': column} in state['obstacles']):
                return 0
    elif dir == "up":
        if row-1 > 0:
            if({'row': row-1, 'column': column} in state['obstacles']):
                return 0
    elif dir == "right":
        if column+1 <= grid.columns:
            if({'row': row, 'column': column+1} in state['obstacles']):
                return 0
    elif dir == "left":
        if column-1 > 0:
            if({'row': row, 'column': column-1} in state['obstacles']):
                return 0
    return 1 

def obstacle_ahead(row = bot.my_row(), column = bot.my_column()):
    state = grid.get_state()
    dir = bot.get_dir()
    if dir == "down":
        if row+1 <= grid.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "up":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "right":
        if column+1 <= grid.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
    elif dir == "left":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
    return 0 

def obstacle_behind(row = bot.my_row(), column = bot.my_column()):
    state = grid.get_state()
    dir = bot.get_dir()
    if dir == "up":
        if row+1 <= grid.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "down":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "left":
        if column+1 <= grid.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
    elif dir == "right":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
    return 0 

def obstacle_left(row = bot.my_row(), column = bot.my_column()):
    state = grid.get_state()
    dir = bot.get_dir()
    if dir == "left":
        if row+1 <= grid.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "right":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "down":
        print(state['obstacles'])
        if column+1 <= grid.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
    elif dir == "up":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
    return 0

def obstacle_right(row = bot.my_row(), column = bot.my_column()):
    state = grid.get_state()
    dir = bot.get_dir()
    if dir == "right":
        if row+1 <= grid.rows:
            if({'position': {'row': row+1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "left":
        if row-1 > 0:
            if({'position': {'row': row-1, 'column': column}} in state['obstacles']):
                return 1
    elif dir == "up":
        if column+1 <= grid.columns:
            if({'position': {'row': row, 'column': column+1}} in state['obstacles']):
                return 1
    elif dir == "down":
        if column-1 > 0:
            if({'position': {'row': row, 'column': column-1}} in state['obstacles']):
                return 1
    return 0 

def print_value(expr):
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    response = expr
    results.append(make_response("value", response))
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def submit(value = None):
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    problem = Problem.get_instance()
    if value is not None:
        response = problem.check_answer(value)
    else:
        current_state = {
            "coin_sweeper": bot.get_state_for_answer(),
            "grid": grid.get_state_for_answer()
        }
        response = problem.check_answer(current_state)
    results.append(make_response("submit", response))
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))
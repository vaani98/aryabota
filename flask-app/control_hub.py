"""Control Hub that makes changes to the CoinSweeper environment - grid and robot"""
"""Writes outcomes to a result file"""
import yaml
import json

from grid import Grid
from coin_sweeper import CoinSweeper

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
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    results.append(make_response("value", bot.my_row()))
    print(results)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def get_my_column():
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    results.append(make_response("value", bot.my_column()))
    print(results)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

def move(steps):
    (success, message) = bot.move(steps)
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
        if success:
            results.append(make_response("state", bot.get_state()))
        else:
            results.append(make_response("error", message))
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

def get_number_of_coins(row = bot.my_row(), column = bot.my_column()):
    # TODO: change to success and message format as with move, GET should never fail silently
    with open(results_file_path) as results_file:
        results = json.loads(results_file.read())
    results.append(make_response("value", grid.get_number_of_coins(row, column)))
    print(results)
    with open(results_file_path, "w") as results_file:
        results_file.write(json.dumps(results))

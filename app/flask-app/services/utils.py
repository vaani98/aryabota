import json
from jsonschema import RefResolver, Draft7Validator

"""Common Utilities"""

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

def lint_problem_grid(problem_grid):
    """Lint problem grid, returns False if there is an error, else the linted grid on success"""
    rows = problem_grid["rows"]
    columns = problem_grid["columns"]
    # total number of rows and columns cannot be negative
    if rows < 1 or columns < 1:
        return False
    start_row = problem_grid["coin_sweeper_start"]["row"]
    start_column = problem_grid["coin_sweeper_start"]["column"]
    start_dir = problem_grid["coin_sweeper_start"]["dir"]
    # CoinSweeper's initial position needs to be somewhere in the grid and direction needs to be correct
    if start_row < 1 or start_row > rows:
        return False
    if start_column < 1 or start_column > columns:
        return False
    if start_dir not in ["up", "down", "left", "right"]:
        return False
    # convert coins and obstacles lists to the per-position format as well
    # also ensure coins and obstacles are in range
    coins = problem_grid["coins"]
    obstacles = problem_grid["obstacles"]
    coins_per_position = get_for_every_position(coins, rows, columns, True)
    obstacles_per_position = get_for_every_position(obstacles, rows, columns, False)
    if coins_per_position is False or obstacles_per_position is False:
        return False
    problem_grid["coins_per_position"] = coins_per_position
    problem_grid["obstacles_per_position"] = obstacles_per_position
    return problem_grid

def get_for_every_position(objects, rows, columns, coins = True):
    """Return values for each position"""
    per_position = [[0 for i in range(columns)] for j in range(rows)]
    for obj in objects:
        loc_row = obj["position"]["row"]
        loc_column = obj["position"]["column"]
        if loc_row < 1 or loc_row > rows:
            return False
        if loc_column < 1 or loc_column > columns:
            return False
        if coins:
            per_position[loc_row - 1][loc_column - 1] = obj["number"]
        else:
            per_position[loc_row - 1][loc_column - 1] = -1
    return per_position

def convert_english_pseudocode_to_python(command, **params):
    """Converting pseudocode to python"""
    # TODO move this table to a JSON/YAML configuration file?
    conversion_table = {
        "MYROW": "get_my_row()",
        "MYCOLUMN": "get_my_column()",
        "TURNLEFT": "turn()",
        "TURNRIGHT": "turn('right')",
        "PENUP": "set_pen('up')",
        "PENDOWN": "set_pen('down')",
        "MOVE": "move({steps})",
        "GET_COINS": "get_number_of_coins()",
        "PLUS": "{variable1}+{variable2}",
        "MINUS": "{variable1}-{variable2}",
        "TIMES": "{variable1}*{variable2}",
        "DIVIDE": "{variable1}/{variable2}",
        "MODULO": "{variable1}%{variable2}",
        "OBSTACLEAHEAD": "obstacle_ahead()",
        "OBSTACLEBEHIND": "obstacle_behind()",
        "OBSTACLELEFT": "obstacle_left()",
        "OBSTACLERIGHT": "obstacle_right()",
        "IF": "if {expr}:",
        "ELSE": "else:",
        "REPEAT": "for repeat in range({times}):",
        "IDENTIFIER" : "{variable}",
        "NUMBER" : "{value}",
        "PRINT_VALUE": "print_value({expr})",
        "ASSIGNMENT": "{variable}={expr}",
        "SUBMIT": "submit({value})",
        "LT": "{variable1}<{variable2}",
        "GT": "{variable1}>{variable2}",
        "LTE": "{variable1}<={variable2}",
        "GTE": "{variable1}>={variable2}",
        "EQUALS": "{variable1}=={variable2}",
        "NOTEQUALS": "{variable1}!={variable2}"
    }
    return conversion_table[command].format(**params)

def convert_kannada_pseudocode_to_python(command, **params):
    """Converting kannada pseudocode to python"""
    # TODO move this table to a JSON/YAML configuration file?
    conversion_table = {
        "MYROW": "get_my_row()",
        "MYCOLUMN": "get_my_column()",
        "TURNLEFT": "turn()",
        "TURNRIGHT": "turn('right')",
        "PENUP": "set_pen('up')",
        "PENDOWN": "set_pen('down')",
        "MOVE": "move({steps})",
        "GET_COINS": "get_number_of_coins()",
        "PLUS": "{variable1}+{variable2}",
        "MINUS": "{variable1}-{variable2}",
        "TIMES": "{variable1}*{variable2}",
        "DIVIDE": "{variable1}/{variable2}",
        "IFCOINS": "if get_number_of_coins()>0:",
        "IFNOOBSTACLE": "if obstacle()==0:",
        "IFOBSTACLEAHEAD": "if obstacle_ahead()==1:",
        "IFOBSTACLEBEHIND": "if obstacle_behind()==1:",
        "IFOBSTACLELEFT": "if obstacle_left()==1:",
        "IFOBSTACLERIGHT": "if obstacle_right()==1:",
        "IDENTIFIER" : "{variable}",
        "NUMBER" : "{value}",
        "PRINT_VALUE": "print_value({expr})",
        "ASSIGNMENT": "{variable}={expr}",
        "SUBMIT": "submit({value})",
        "LT": "{variable1}<{variable2}",
        "GT": "{variable1}>{variable2}",
        "LTE": "{variable1}<={variable2}",
        "GTE": "{variable1}>={variable2}",
        "EQUALS": "{variable1}=={variable2}",
        "NOTEQUALS": "{variable1}!={variable2}"
    }
    return conversion_table[command].format(**params)

def convert_kanglish_pseudocode_to_python(command, **params):
    """Converting Kanglish pseudocode to python"""
    # TODO move this table to a JSON/YAML configuration file?
    conversion_table = {
        "MYROW": "get_my_row()",
        "MYCOLUMN": "get_my_column()",
        "TURNLEFT": "turn()",
        "TURNRIGHT": "turn('right')",
        "PENUP": "set_pen('up')",
        "PENDOWN": "set_pen('down')",
        "MOVE": "move({steps})",
        "GET_COINS": "get_number_of_coins()",
        "PLUS": "{variable1}+{variable2}",
        "MINUS": "{variable1}-{variable2}",
        "TIMES": "{variable1}*{variable2}",
        "DIVIDE": "{variable1}/{variable2}",
        "IFCOINS": "if get_number_of_coins()>0:",
        "IFNOOBSTACLE": "if obstacle()==0:",
        "IFOBSTACLEAHEAD": "if obstacle_ahead()==1:",
        "IFOBSTACLEBEHIND": "if obstacle_behind()==1:",
        "IFOBSTACLELEFT": "if obstacle_left()==1:",
        "IFOBSTACLERIGHT": "if obstacle_right()==1:",
        "IDENTIFIER" : "{variable}",
        "NUMBER" : "{value}",
        "PRINT_VALUE": "print_value({expr})",
        "ASSIGNMENT": "{variable}={expr}",
        "SUBMIT": "submit({value})",
        "LT": "{variable1}<{variable2}",
        "GT": "{variable1}>{variable2}",
        "LTE": "{variable1}<={variable2}",
        "GTE": "{variable1}>={variable2}",
        "EQUALS": "{variable1}=={variable2}",
        "NOTEQUALS": "{variable1}!={variable2}"
    }
    return conversion_table[command].format(**params)

"""Common Utilities"""

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
    per_position = [[0 for i in range(columns)] for j in range(rows)]
    for loc in objects:
        loc_row = loc["row"]
        loc_column = loc["column"]
        if loc_row < 1 or loc_row > rows:
            return False
        if loc_column < 1 or loc_column > columns:
            return False
        if coins:
            per_position[loc_row - 1][loc_column - 1] = loc["value"]
        else:
            per_position[loc_row - 1][loc_column - 1] = -1
    return per_position

def convert_pseudocode_to_python(command, **params):
    # TODO move this table to a JSON/YAML configuration file?
    conversion_table = {
        "MYROW": "get_my_row()",
        "MYCOLUMN": "get_my_column()",
        "TURNLEFT": "turn()",
        "TURNRIGHT": "turn(direction='right')",
        "MOVE": "move({steps})"
    }
    return conversion_table[command].format(**params)
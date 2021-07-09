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
    # convert coins list to the required format
    coins = problem_grid["coins"]
    coins_per_position = [[0 for i in range(columns)] for j in range(rows)]
    for loc in coins:
        loc_row = loc["row"]
        loc_column = loc["column"]
        # ensure coins loc is in the grid
        if loc_row < 1 or loc_row > rows:
            return False
        if loc_column < 1 or loc_column > columns:
            return False
        coins_per_position[loc_row - 1][loc_column - 1] = loc["value"]
    problem_grid["coins_per_position"] = coins_per_position
    return problem_grid

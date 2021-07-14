"""Control Hub that makes changes to the CoinSweeper environment - grid and robot"""
from grid import Grid
from coin_sweeper import CoinSweeper

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

def get_my_row():
    return ("value", bot.my_row())

def get_my_column():
    return ("value", bot.my_column())

def move(steps):
    (success, message) = bot.move(steps)
    if success:
        return ("state", [bot.get_state()])
    else:
        return ("error", message)

def turn(direction = "left"):
    if direction == "left":
        bot.turn_left()
    elif direction == "right":
        bot.turn_right()
    return ("state", [bot.get_state()])

def get_number_of_coins(row = bot.my_row(), column = bot.my_column()):
    # TODO: change to success and message format as with move, GET should never fail silently
    return ("value", grid.get_number_of_coins(row, column))

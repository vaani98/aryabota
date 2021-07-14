"""Control Hub that makes changes to the CoinSweeper environment - grid and robot"""
from grid import Grid
from coin_sweeper import CoinSweeper

bot = CoinSweeper.get_instance()
grid = Grid.get_instance()

def get_my_row():
    return bot.my_row()

def get_my_column():
    return bot.my_column()

def move(steps):
    (success, message) = bot.move(steps)

def turn(direction = "left"):
    if direction == "left":
        bot.turn_left()
    elif direction == "right":
        bot.turn_right()
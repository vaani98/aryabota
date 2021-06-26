# intro-to-programming
Tool for teaching introduction to programming

# Using the virtual environment
1. Create the virtual environment called `venv` by running `virtualenv venv`, it should create a directory called `venv` at the root-level
1. On Linux-based OS, run `source venv/bin/activate`
2. To deactivate, run `deactivate`

As of now, probably only need to install PLY, `pip install ply`.

## Iteration 1: BotZero (command line tool)
BotZero is a robot in a grid. Its position is defined by its coordinates as in a Cartesian plane. The direction it is facing can be `left`, `right`, `up` or `down`.  

Initial position: `0, 0, up`

For this iteration, we will assume that the grid does not have any obstacles or walls - it's just the Cartesian plane.

### Commands
1. `My X`: What is the bot's x-coordinate?
2. `My Y`: What is the bot's y-coordinate?
3. `Move 10`: Move the bot 10 steps in the direction it is facing.
4. `Turn left`: Turn the bot towards its left (by 90 degrees).
5. `Exit`: Exit the program.

## Iteration 2: CoinSweeper (web app)
### v1
Same features as BotZero, except in a web application. Also converts pseudo-code to Python intermediate code and outputs the same.
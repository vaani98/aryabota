# CoinSweeper
A visual tool for teaching introduction to programming, that slowly allows students to transition from using commands similar to natural language, to more Pythonic constructs.   
The experience is gamified through a visual component called CoinSweeper - a bot in a grid that detects and picks up coins while navigating its way around obstacles.
This tool is still under development; you can track the progress via the [changelog](https://github.com/vaani98/coinsweeper/blob/flask-branch/changelog.md).

## Set-Up
### Virtual Environment
1. Create the virtual environment called `venv` by running `virtualenv venv`, it should create a directory called `venv` at the root-level
1. On Linux-based OS, run `source venv/bin/activate`
2. To deactivate, run `deactivate`
### Dependencies
1. Python3: install the required PyPi packages by running  
 `python3 -m pip install -r requirements.txt`

## Running the App
1. Start the server in development mode by running  
`FLASK_ENV=development flask run`

### Environment
The CoinSweeper bot is present in a grid that resembles the Cartesian plane. It has x and y coordinates. The direction it is facing can be `left`, `right`, `up` or `down`.

### Initial Position
`0, 0, left`

### Commands
1. `My X`: What is the bot's x-coordinate?
2. `My Y`: What is the bot's y-coordinate?
3. `Move 10`: Move the bot 10 steps in the direction it is facing.
4. `Turn left`: Turn the bot towards its left (by 90 degrees).

## Resources
* [API Reference](https://www.notion.so/API-Documentation-CoinSweeper-v1-a56d56379e8b4adb9fd00a5b9564e371)
* [Postman Collection](https://www.getpostman.com/collections/56feaa2f2b576456562a)

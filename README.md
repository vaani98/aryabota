# CoinSweeper
A visual tool for teaching introduction to programming, that slowly allows students to transition from using commands similar to natural language, to more Pythonic constructs.   
The experience is gamified through a visual component called CoinSweeper - a bot in a grid that detects and picks up coins while navigating its way around obstacles.
This tool is still under development; you can track the progress via the [changelog](https://github.com/vaani98/coinsweeper/blob/flask-branch/changelog.md).

## Set-Up
### Virtual Environment
1. Create the virtual environment called `venv` by running `virtualenv venv`, it should create a directory called `venv` at the root-level
1. On Linux-based OS, run `source venv/bin/activate`; on Windows, run `.\env\Scripts\activate`
2. To deactivate, run `deactivate`
### Dependencies
1. Python3: install the required PyPi packages by running  
 `python3 -m pip install -r requirements.txt`

## Running the Server
1. Start the server in development mode by running  
`FLASK_ENV=development flask run`

## Setting up the React App
1. In the `grid-ui` directory, run `npm install` to install the dependencies
2. To start the web app UI, run `npm start`

### Commands
1. `My Row`: What row is the bot in?
2. `My Column`: What column is the bot in?
3. `Move 10`: Move the bot 10 steps in the direction it is facing.
4. `Turn left`: Turn the bot towards its left (by 90 degrees).

## Resources
* [API Reference](https://www.notion.so/API-Documentation-CoinSweeper-v1-a56d56379e8b4adb9fd00a5b9564e371)
* [Postman Collection](https://www.getpostman.com/collections/56feaa2f2b576456562a)

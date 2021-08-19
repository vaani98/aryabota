# CoinSweeper
A visual tool for teaching introduction to programming, that slowly allows students to transition from using commands similar to natural language, to more Pythonic constructs.   
The experience is gamified through a visual component called CoinSweeper - a bot in a grid that detects and picks up coins while navigating its way around obstacles.
This tool is still under development. For further documentation, see [here](https://gem-gerbera-5fd.notion.site/CoinSweeper-316098bf36fc4cef9aeb8ef884a8c2d3).

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

## How To
Visit the documentation [here](https://gem-gerbera-5fd.notion.site/CoinSweeper-316098bf36fc4cef9aeb8ef884a8c2d3).

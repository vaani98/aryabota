# CoinSweeper
A visual tool for teaching introduction to programming, that slowly allows students to transition from using commands similar to natural language, to more Pythonic constructs.   
The experience is gamified through a visual component called CoinSweeper - a bot in a grid that detects and picks up coins while navigating its way around obstacles.
This tool is still under development.

## Set-Up - With Docker
Docker Version `20.10.7`  
In the root directory of this project, run  
`docker-compose up --build`  
Visit `localhost:80` to start using the app!

## Set-Up - Without Docker
### Virtual Environment for Server
1. Create the virtual environment called `venv` by running `virtualenv venv`, it should create a directory called `venv` at the root-level
1. On Linux-based OS, run `source venv/bin/activate`; on Windows, run `.\env\Scripts\activate`
2. To deactivate, run `deactivate`
### Dependencies for Server
1. Python3: install the required PyPi packages by running the following in `app/flask-app`  
 `python3 -m pip install -r requirements.txt`
### Running the Server
1. Start the server in development mode by running the following in `app/flask-app`  
`FLASK_ENV=development flask run`
### Dependencies for the React App
1. In the `app/grid-ui` directory, run `npm install` to install the dependencies
### Starting the React App
1. In the `app/grid-ui` directory, run `npm start` to start the web UI

## How To
Visit the documentation [here](https://gem-gerbera-5fd.notion.site/CoinSweeper-316098bf36fc4cef9aeb8ef884a8c2d3).

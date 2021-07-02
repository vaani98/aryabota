import ReactDOM from 'react-dom';
import './index.css';
import React, { useState, useLayoutEffect} from 'react';
//UTILITY FUNCTIONS SCRIPT
import { randomPositions } from './utils';
//MAZE GENERATOR COMPONENT
import Maze from './mazeGenerator';
//CHARACTER CONTROLLER COMPONENT
import Controller from './characterController';
//GLOBAL CONTEXT / STATE
import { MazeState } from './globalStates';


let input = {
  x: 10,
  y: 10
}

/**
 * generate a ~center location for character and 
 * random locations for food.
 * @returns [array of numbers], number 
 */
const randomFoods = randomPositions(parseInt(input.x), parseInt(input.y));
const centreMario = 1;


/**
 * Main Game Component
 * This component:
 * 1. initialize global state
 * 2. wrap that global state on maze and controller
 * 3. serve main page html
 * @component
 * @example
 * <Game />
 */
function Game() {

  /**
   * Global state to initialize.
   * @const
   */
  const [mazeData, setMazeData] = useState({});

  /**
   * Game's useEffect 
   * This initialize all global state variables
   * @public
   */
  useLayoutEffect(() => {
    setMazeData(mazeData => ({
      ...mazeData, 
      randomFoods: randomFoods,
      marioLoc: centreMario,
      inputX: parseInt(input.x),
      inputY: parseInt(input.y),
      currentDirection: null,
      score: 0
    }));

  }, []);

  //check if player location is generated
  let maze, score = mazeData.score;
  if(mazeData.marioLoc){
    //set maze and controller component with required props
    maze =(
      <MazeState.Provider value={[mazeData, setMazeData]}>
        <Maze x={input.x} y={input.y} foodLoc={mazeData.randomFoods} marioLoc={mazeData.marioLoc} />
        <Controller />
      </MazeState.Provider>
    );
  } else {
    maze = <p>Loading</p>
  }

  return (
    <div className="game">
      <div className="game-maze">
        {maze}
      </div>
    </div>
  );
}


ReactDOM.render(
  <Game />,
  document.getElementById('root')
);
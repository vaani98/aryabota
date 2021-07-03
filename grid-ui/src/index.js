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
   * mazeData contains the entire state of the maze
   * @const
   */
  const [mazeData, setMazeData] = useState({});

  /**
   * Game's useEffect:
   * this initializes mazeData
   * @public
   */
  useLayoutEffect(() => {
    setMazeData(mazeData => ({
      ...mazeData,
      marioLoc: 1,
      inputX: parseInt(input.x),
      inputY: parseInt(input.y),
      randomFoods: randomFoods,
      currentDirection: "down"
    }));

  }, []);

  //check if player location is generated
  let maze;
  if(mazeData.marioLoc){
    //set maze and controller component with required props
    maze = (
        <div className = "game">
          <MazeState.Provider value={[mazeData, setMazeData]}>
            <Controller />
            <Maze 
              x = {input.x} 
              y = {input.y} 
              foodLoc = {mazeData.randomFoods} 
              marioLoc = {mazeData.marioLoc} 
              currentDirection = {mazeData.currentDirection} />
          </MazeState.Provider>
        </div>
    );
  } else {
    maze = <p>Loading...</p>
  }

  return (
    <>
        { maze }
    </>
  );
}
ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

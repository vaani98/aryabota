import ReactDOM from 'react-dom';
import './index.css';
import React, { useState, useLayoutEffect} from 'react';
//UTILITY FUNCTIONS SCRIPT
import { randomPositions, convertToContinuousNumbering } from './utils';
//MAZE GENERATOR COMPONENT
import Maze from './mazeGenerator';
//CHARACTER CONTROLLER COMPONENT
import Controller from './characterController';
//GLOBAL CONTEXT / STATE
import { MazeState } from './globalStates';

/**
 * generate a ~center location for character and 
 * random locations for food.
 * @returns [array of numbers], number 
 */
const randomFoods = randomPositions(3, 3);


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
    /**
     * making request to get initial state of the grid and CoinSweeper robot 
     */
    fetch('http://localhost:5000/coinSweeper', {
    crossDomain: true,
    method: 'GET',
    headers: {
          'Content-type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(response => {
      setMazeData(mazeData => ({
        ...mazeData,
        inputX: response.rows,
        inputY: response.columns,
        marioLoc: convertToContinuousNumbering(response.row, response.column, response.columns),
        randomFoods: response.coins.map(obj => convertToContinuousNumbering(obj.row, obj.column, response.columns)),
        positionsSeen: [1]
      }))
    });
  }, []);

  //check if player location is generated
  let maze;
  if(mazeData.marioLoc) {
    console.log(mazeData)
    //set maze and controller component with required props
    maze = (
        <div className = "game">
          <MazeState.Provider value={[mazeData, setMazeData]}>
            <Controller />
            <Maze 
              x = {mazeData.inputX} 
              y = {mazeData.inputY}
              foodLoc = {mazeData.randomFoods} 
              marioLoc = {mazeData.marioLoc} 
              currentDirection = {mazeData.currentDirection}
              positionsSeen = {mazeData.positionsSeen}
              />
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

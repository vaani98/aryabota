import ReactDOM from 'react-dom';
import './styles/index.css';
import React, { useState, useLayoutEffect } from 'react';
//UTILITY FUNCTIONS SCRIPT
import { randomPositions, convertToContinuousNumbering } from './utils';
//MAZE GENERATOR COMPONENT
import Maze from './mazeGenerator';
//CHARACTER CONTROLLER COMPONENT
import Controller from './characterController';
import MessageModal from './modals/MessageModal';
//GLOBAL CONTEXT / STATE
import { MazeState, Constants } from './globalStates';
import LevelMap from './levelMap';

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
          rows: response?.rows,
          columns: response?.columns,
          coinSweeper: convertToContinuousNumbering(response?.row, response?.column, response?.columns),
          coinLoc: response?.coins?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
          obstacleLoc: response?.obstacles?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
          positionsSeen: response?.trail?.map(trailObj => convertToContinuousNumbering(trailObj?.row, trailObj?.column, response?.columns)),
          currentDirection: response?.dir,
          levelType: response?.type,
          home: response?.homes?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
          statement: response?.statement,
          problemSpec: response?.problem_spec,
          //TODO: Might want to set these two values from backend
          penLoc: [1],
          prevSteps: 1,
          infoMessage: { show: true, message: Constants.informationMessage }
        }))
      });
  }, []);

  //check if player location is generated
  let maze;
  let messageModal = null;
  if (mazeData.error_message || mazeData.message || mazeData.infoMessage?.show) {
    const modalMessage = mazeData.error_message
      ? mazeData.error_message
      : mazeData.infoMessage.show
        ? mazeData.infoMessage.message
        : mazeData.message;
    messageModal = <MessageModal error_message={modalMessage} />;
  }
  if (mazeData.coinSweeper) {
    //set maze and controller component with required props
    maze = (
      <>
        <div className="game">
          <MazeState.Provider value={[mazeData, setMazeData]}>
            {messageModal}
            <Controller />
          </MazeState.Provider>
        </div>
      </>
    );
  } else {
    maze = <p>Loading...</p>
  }

  return (
    <>
      {maze}
    </>
  );
}
ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

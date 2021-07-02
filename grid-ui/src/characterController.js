import React, { useContext, useEffect, useState, useLayoutEffect } from 'react';
//GLOBAL CONTEXT / STATE
import { MazeState } from './globalStates';

/**
 * Component for controlling character/player
 * This component:
 * 1. take movement input to move player correctly
 * 2. take care of maze boundaries
 * 3. handles eating food 
 * 4. updates winning condition and score
 * @component
 * @example
 * <Controller />
 */
export default function Controller() {
    /**
     * Global context / state to manipulate character location, etc.
     * @const
     */
    const [mazeData, setMazeData] = useContext(MazeState);
    
    /**
     * local state to store interval id / game loop id
     * @const
     */
    const [control, setControl] = useState({
        gameInterval: null
    });

    /**
     * Controller's useLayoutEffect 
     * This checks winning condition
     * ( if food item array is smaller than 1 )
     * @public
     */
    useLayoutEffect(() => {
        if( mazeData.randomFoods.length < 1){
            //clear interval /game loop
            clearInterval(control.gameInterval);
            //alert result
            alert("You did it in " + mazeData.score + " Steps");
        }
    }, [mazeData, control]);


    /**
     * Controller's useEffect
     * Step 1: This checks if character is at food location and 
     * if so then eat it(remove from food array).
     * Step 2: Check if character is overflowing out of maze boundary.
     * @public
     */
    useEffect(() => {
        
        const found = mazeData.randomFoods.indexOf(mazeData.marioLoc);
        if(found !==-1){
            const updatedFood = mazeData.randomFoods.filter((item) => item!== (mazeData.marioLoc));
            setMazeData(prev => ({
                ...prev,
                randomFoods: updatedFood
            }));
        }

        //check if character is overflowing maze
        isBoundary();
    
    }, [mazeData, setMazeData]);

    /**
     * function to move player one step RIGHT
     * and increase score/ total steps by one
     * @public
     */
    const moveRight = () => {
        setMazeData(prev => ({
            ...prev,
            marioLoc: prev.marioLoc + 1,
            currentDirection: 'right',
            score: prev.score +1
        }));
    }
  
    /**
     * function to move player one step LEFT
     * and increase score/ total steps by one
     * @public
     */
    const moveLeft = () => {
        setMazeData(prev => ({
            ...prev,
            marioLoc: prev.marioLoc - 1,
            currentDirection: 'left',
            score: prev.score +1
        }));
    }

    /**
     * function to move player one step UP
     * and increase score/ total steps by one
     * LOGIC: WE ARE SUBTRACTING 1 ROW FROM CURRENT
     * POSITION OF CHARACTER TO SIMULATE ONE STEP UP
     * @public
     */
    const moveUp = () => {
        setMazeData(prev => ({
            ...prev,
            marioLoc: prev.marioLoc - prev.inputX,
            currentDirection: 'up',
            score: prev.score +1
        }));
    }
    
    /**
     * function to move player one step DOWN
     * and increase score/ total steps by one
     * LOGIC: WE ARE ADDING 1 ROW IN CURRENT
     * POSITION OF CHARACTER TO SIMULATE ONE STEP DOWN
     * @public
     */
    const moveDown = () => {
        setMazeData(prev => ({
            ...prev,
            marioLoc: prev.marioLoc + prev.inputX,
            currentDirection: 'down',
            score: prev.score +1
        }));
    }

    /**
     * Function to check if boundaries character is gonna
     * overflow boundary, if so then move it in opposite direction
     * LOGIC: IT CHECKS IF CHARACTER LOCATION IS NEAR BOUNDARY "AND"
     * IF CURRENT DIRECTION OF MOVEMENT IS GOING OUT BOUNDARY ONLY
     * THEN IT CHANGES THE DIRECTION TO OPPOSITE SIDE
     * @public
     */
    const isBoundary = () => {
        if(mazeData.marioLoc + mazeData.inputX > mazeData.inputX * mazeData.inputY && mazeData.currentDirection==='down'){
            gameLoop(moveUp);    
            return;
        }else if(mazeData.marioLoc - mazeData.inputX < 0 && mazeData.currentDirection==='up'){
            gameLoop(moveDown);    
            return;
        }else if((mazeData.marioLoc - 1)%mazeData.inputX === 0 && mazeData.currentDirection==='left'){
            gameLoop(moveRight);    
            return;
        }else if((mazeData.marioLoc)%mazeData.inputX === 0 && mazeData.currentDirection==='right'){
            gameLoop(moveLeft);    
            return;
        }
    }

    return (
      <div className="controller"></div>
    );
}
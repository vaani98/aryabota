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

    return (
      <div className="controller"></div>
    );
}
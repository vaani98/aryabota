import React, { useContext, useEffect, useState } from 'react';
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
    // const [pythonicCode, setPythonicCode] = useContext(PythonicCodeState);
    
    /**
     * local state to store interval id / game loop id
     * @const
     */
    const [control, setControl] = useState({
        changeInterval: null,
        pythonicCode: [],
        steps: []
    });

    useEffect(() => {
        if (control.steps.length && control.changeInterval == null) {
            control.changeInterval = setInterval(doChange, 600)
        }
    });

    function doChange() {
        if (control.steps.length > 0)
        {
            const currStep = control.steps[0]
            if (currStep.stateChanges.length > 0) {
                const change = currStep.stateChanges[0]
                setMazeData(prev => ({
                    ...prev,
                    ...change
                }))
                currStep.stateChanges.shift()
            } else {
                control.pythonicCode.push(currStep.python)
                control.steps.shift()
            }
        } else {
            clearInterval(control.changeInterval)
            setControl(prev => ({
                ...prev,
                changeInterval: null
            }))
        }
        
    }
    
    function updateCoinSweeperBot(code) {
        const steps = getSteps(code, mazeData);
        console.log(steps)
        setControl(prev => ({
            ...prev,
            steps: steps
        }));
    }

    function getSteps(code, currState) {
        // TODO replace below with API call to get response
        const response = 
        [
            {
                "python": "move(3)",
                "stateChanges": [
                    {
                        "x": 1,
                        "y": 4,
                        "dir": "down"
                    }
                ]   
            },
            {
                "python": "turnLeft()",
                "stateChanges": [
                    {
                        "x": 1,
                        "y": 4,
                        "dir": "left"
                    }
                ]
            },
            {
                "python": "turnLeft()",
                "stateChanges": [
                    {
                        "x": 1,
                        "y": 4,
                        "dir": "up"
                    }
                ]
            },
            {
                "python": "turnLeft()",
                "stateChanges": [
                    {
                        "x": 1,
                        "y": 4,
                        "dir": "right"
                    }
                ]
            },
            {
                "python": "move(5)",
                "stateChanges": [
                    {
                        "x": 6,
                        "y": 4,
                        "dir": "right"
                    }
                ] 
            }
        ];
        let steps = [];
        response.forEach(step => {
            let stepObj = {
                python: step.python,
                stateChanges: []
            };
            step.stateChanges.forEach(change => {
                const newPos = convertToContinuousNumbering(change.x, change.y, currState.inputY);
                const newDir = change.dir;
                const newPositionsSeen = convertPositions(newPos, currState.marioLoc, currState.inputY);
                console.log(newPositionsSeen);
                currState = {
                    ...currState,
                    marioLoc: newPos,
                    currentDirection: newDir,
                    positionsSeen: currState.positionsSeen.concat(newPositionsSeen),
                };
                stepObj.stateChanges.push(currState);
            });
            steps.push(stepObj);
        })
        return steps;
    }

    function range(size, startAt = 0) {
        return [...Array(size).keys()].map(i => i + startAt);
    }

    function convertPositions(newPos, oldPos, columns) {
        let newPosCoordinates = convertToCoordinates(newPos, columns);
        let oldPosCoordinates = convertToCoordinates(oldPos, columns);
        if (oldPosCoordinates.y == newPosCoordinates.y) {
            return range(newPos - oldPos + 1, oldPos)
        } else if (oldPosCoordinates.x == newPosCoordinates.x) {
            let yrange = range(newPosCoordinates.y - oldPosCoordinates.y + 1, oldPosCoordinates.y)
            return yrange.map(yvalue => convertToContinuousNumbering(oldPosCoordinates.x, yvalue, columns))
        } else {
            return []
        }
    }

    function getPythonicCode() {
        return <div><br/>
           {control.pythonicCode.map(codeLine => {
               return <p> {codeLine} </p>
           })}
        </div>
    }

    function convertToCoordinates(blockCount, columns) {
        const y = 1 + Math.floor(blockCount / columns);
        const x = blockCount % columns;
        return { x, y }
    }

    function convertToContinuousNumbering(x, y, columns) {
        let conv = (x + columns * (y - 1));
        return conv
    }

    const submitCode = function(e) {
        e.preventDefault();
        const code = e.target[0].value;
        updateCoinSweeperBot(code)
    }

    return (
        <>
            <div className = "game-info">
                <form onSubmit = {submitCode}>
                    <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        marginRight: '50px'
                    }}>
                        <textarea rows="20" cols="50" />
                    </div>
                    <input type = "submit" value = "Run"/>
                </form>
            </div>
            <div className = "separator"></div>
            <div className = "game-info">
                <h3>Translated Code: Python</h3>
                { getPythonicCode() }
            </div>
            <div className = "separator"></div>
            <div className="controller"></div>
      </>
    );
}
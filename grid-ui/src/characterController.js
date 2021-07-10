import React, { useContext, useEffect, useState } from 'react';
//GLOBAL CONTEXT / STATE
import { MazeState } from './globalStates';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import { blueGrey } from '@material-ui/core/colors';
import Button from '@material-ui/core/Button';
import PlayArrowRounded from '@material-ui/icons/PlayArrowRounded';

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
        if (control.steps.length > 0) {
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
        getSteps(code, mazeData);
    }

    function getSteps(code, currState) {
        fetch('http://localhost:5000/coinSweeper', {
            crossDomain: true,
            method: 'POST',
            body: JSON.stringify(code),
            headers: {
                'Content-type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(response => {
                let steps = [];
                response.forEach(step => {
                    let stepObj = {
                        python: step.python,
                        stateChanges: []
                    };
                    step.stateChanges.forEach(change => {
                        const newPos = convertToContinuousNumbering(change.row, change.column, currState.inputY);
                        const newDir = change.dir;
                        const newPositionsSeen = []
                        // convertPositions(newPos, currState.marioLoc, currState.inputY);
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
                setControl(prev => ({
                    ...prev,
                    steps: steps
                }));
            });
    }

    function range(size, startAt = 0) {
        return [...Array(size).keys()].map(i => i + startAt);
    }

    function convertPositions(newPos, oldPos, columns) {
        let newPosCoordinates = convertToCoordinates(newPos, columns);
        let oldPosCoordinates = convertToCoordinates(oldPos, columns);
        if (oldPosCoordinates.y === newPosCoordinates.y) {
            return range(newPos - oldPos + 1, oldPos)
        } else if (oldPosCoordinates.x === newPosCoordinates.x) {
            let yrange = range(newPosCoordinates.y - oldPosCoordinates.y + 1, oldPosCoordinates.y)
            return yrange.map(yvalue => convertToContinuousNumbering(oldPosCoordinates.x, yvalue, columns))
        } else {
            return []
        }
    }

    function getPythonicCode() {
        return <div>
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

    function convertToContinuousNumbering(row, column, columns) {
        return column + columns * (row - 1);
    }

    const submitCode = function (e) {
        e.preventDefault();
        const code = e.target[0].value;
        updateCoinSweeperBot(code)
    }

    const theme = createTheme({
        palette: {
            primary: blueGrey,
        },
    });

    return (
        <>
            <div className="game-info">
                <h3>Enter your code here:</h3>
                <div className="input-div">
                    <form onSubmit={submitCode}>
                        <div style={{
                            display: 'flex',
                            flexDirection: 'column',
                            marginRight: '50px'
                        }}>
                            <textarea />
                        </div>

                        <ThemeProvider theme={theme}>
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                endIcon={<PlayArrowRounded />}
                            >
                                Run
                            </Button>
                        </ThemeProvider>
                    </form>
                    <div className="output-div">
                        <h3 className="output-title">Output:</h3>
                        <div></div>
                    </div>
                </div>
            </div>
            <div className="separator"></div>
            <div className="game-info">
                <h3>Translated Code: Python</h3>
                <br />
                {getPythonicCode()}
            </div>
            <div className="separator"></div>
            <div className="controller"></div>
        </>
    );
}
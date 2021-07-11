import React, { useContext, useEffect, useState } from 'react';
//GLOBAL CONTEXT / STATE
import { MazeState } from './globalStates';
import { convertToContinuousNumbering } from './utils';
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
        outputValue: [],
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
            if (currStep?.stateChanges?.length > 0) {
                const change = currStep.stateChanges[0]
                setMazeData(prev => ({
                    ...prev,
                    ...change,
                    error_message: null,
                }))
                currStep.stateChanges.shift()
            } else if (currStep.error_message) {
                setMazeData(prev => ({
                    ...prev,
                    error_message: currStep.error_message
                }))
                control.steps.shift();
            } else {
                control.pythonicCode.push(currStep.python)
                control.outputValue.push(currStep.outputValue)
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
            console.log(response)
            let steps = [];
            response.forEach(step => {
                console.log(step)
                if(step.error_message) {
                    steps.push({
                        error_message: step.error_message
                    });
                    setControl(prev => ({
                        ...prev,
                        steps: steps
                    }));
                    throw "obstacle/boundary error";
                }
                if ("python" in step) {
                    if ("value" in step) {
                        let stepObj = {
                            python: step.python,
                            outputValue: step.value
                        };
                        steps.push(stepObj)
                        setControl(prev => ({
                            ...prev,
                            steps: steps
                        }));
                    } else if ("stateChanges" in step) {
                        let stepObj = {
                            python: step.python,
                            stateChanges: []
                        };
                        step.stateChanges?.forEach(change => {
                            const newPos = convertToContinuousNumbering(change.row, change.column, currState.inputY);
                            const newDir = change.dir;
                            const newPositionsSeen = change.trail.map(trailObj => convertToContinuousNumbering(trailObj.row, trailObj.column, currState.inputY));
                            currState = {
                                ...currState,
                                marioLoc: newPos,
                                currentDirection: newDir,
                                positionsSeen: currState.positionsSeen.concat(newPositionsSeen),
                            };
                            stepObj.stateChanges.push(currState);
                        });
                        steps.push(stepObj);
                        setControl(prev => ({
                            ...prev,
                            steps: steps
                        }));
                    }
                }
            })
        });
    }

    function getPythonicCode() {
        return <div>
            {control.pythonicCode.map(codeLine => {
                return <p> {codeLine} </p>
            })}
        </div>
    }

    function getOutputValue() {
        return <div>
            {control.outputValue.map(codeLine => {
            return <p> {codeLine} </p>
        })}
        </div>
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
                        {getOutputValue()}
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
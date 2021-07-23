import React, { useContext, useEffect, useState } from 'react';
import AceEditor from "react-ace";
import "ace-builds/src-noconflict/mode-java";
import "ace-builds/src-noconflict/theme-github";
import './styles/characterController.css';
//GLOBAL CONTEXT / STATE
import { MazeState } from './globalStates';
import { convertToContinuousNumbering } from './utils';
import UiConfigs from './uiConfigurations';
import { createTheme, ThemeProvider } from '@material-ui/core/styles';
import { blueGrey } from '@material-ui/core/colors';
import Button from '@material-ui/core/Button';
import PlayArrowRounded from '@material-ui/icons/PlayArrowRounded';
import Maze from './mazeGenerator';

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

    const [penState, setPenState] = useState("penDown");

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
                    if (step.error_message) {
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
                                    penLoc: penState === "penDown" ? currState.penLoc.concat(newPositionsSeen.slice(currState.prevSteps + 1)) : currState.penLoc,
                                    prevSteps: newPositionsSeen.length
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
        let pythonCode = control.pythonicCode.toString();
        pythonCode = pythonCode.replace(/,/g, '\n');
        // return <div>
        //     {control.pythonicCode.map(codeLine => {
        //         return <p> {codeLine} </p>
        //     })}
        // </div>
        return pythonCode;
    }

    function getOutputValue() {
        let output = control.outputValue.toString();
        //TODO: If someone can make this code better, pls do
        output = output.replace(/,/g, '\n');
        output = output.replace(/\n\n*/g,'\n');
        output = output.replace(/^\s*\n+|\s*\n+$/g,'');
        return output;

        // return <div>
        //     {control.outputValue.map(codeLine => {
        //         return <p> {codeLine} </p>
        //     })}
        // </div>
    }

    const submitCode = function (e) {
        e.preventDefault();
        updateCoinSweeperBot(editorValue);
    }

    const theme = createTheme({
        palette: {
            primary: blueGrey,
        },
    });

    let [editorValue, setEditorValue] = useState('');
    function onChange(newValue) {
        setEditorValue(newValue);
    }

    return (
        <>
            <UiConfigs
                penLoc={mazeData.penLoc}
                onPenChange={setPenState}
            />

            <div className="game-info">
                <h3>Enter your code here:</h3>
                <div className="input-div">
                    <form onSubmit={submitCode}>
                        <div style={{
                            // display: 'flex',
                            // flexDirection: 'column',
                            marginRight: '50px'
                        }}>
                            <AceEditor
                                style={{
                                    width: '116%',
                                    height: '300px'
                                }}
                                classname="editor"
                                mode="java"
                                theme="github"
                                // value={'move 1'}
                                onChange={onChange}
                                name="editor-div"
                                editorProps={{ $blockScrolling: true }}
                            />
                        </div>

                        <ThemeProvider theme={theme}>
                            <Button
                                style={{
                                    marginTop: '30px',
                                    float: 'right',
                                    marginRight: '4%'
                                }}
                                type="submit"
                                variant="contained"
                                color="primary"
                                endIcon={<PlayArrowRounded />}
                            >
                                Run
                            </Button>
                        </ThemeProvider>
                    </form>
                </div>
            </div>
            <div className="separator"></div>
            <div>
                <Maze
                    x={mazeData.inputX}
                    y={mazeData.inputY}
                    coinLoc={mazeData.coinLoc}
                    obstacleLoc={mazeData.obstacleLoc}
                    marioLoc={mazeData.marioLoc}
                    currentDirection={mazeData.currentDirection}
                    positionsSeen={mazeData.positionsSeen}
                    penLoc={mazeData.penLoc}
                    prevSteps={mazeData.prevSteps}
                />
                <div className="output-div">
                    <h3 className="output-title">Output:</h3>
                    <AceEditor
                    style={{
                        width: '100%',
                        height: '100px'
                    }}
                    classname="editor"
                    mode="java"
                    theme="github"
                    value={getOutputValue()}
                    readOnly={true}
                    name="output-div"
                    editorProps={{ $blockScrolling: true }}
                />
                </div>
            </div>
            <div className="separator"></div>
            <div className="game-info">
                <h3>Translated Code: Python</h3>
                <AceEditor
                    style={{
                        width: '100%',
                        height: '300px'
                    }}
                    classname="editor"
                    mode="java"
                    theme="github"
                    value={getPythonicCode()}
                    readOnly={true}
                    name="python-div"
                    editorProps={{ $blockScrolling: true }}
                />
                <ThemeProvider theme={theme}>
                            <Button
                                style={{
                                    marginTop: '30px',
                                    width: '110px',
                                    marginLeft: '65%'
                                }}
                                type="submit"
                                variant="contained"
                                color="primary"
                                endIcon={<PlayArrowRounded />}
                            >
                                Submit
                            </Button>
                        </ThemeProvider>
            </div>
            <div className="controller"></div>
        </>
    );
}
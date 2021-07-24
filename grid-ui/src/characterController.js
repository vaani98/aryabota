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
    const [editorFont, setEditorFont] = useState(14);

    /**
     * local state to store interval id / game loop id
     * @const
     */
    const [control, setControl] = useState({
        changeInterval: null,
        pythonicCode: null,
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

    function parseResponse(response, currState) {
        setControl(prev => ({
            ...prev,
            pythonicCode: response.python
        }))
        let steps = [];
        response.response?.forEach(step => {
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
            if ("value" in step) {
                let stepObj = {
                    outputValue: step.value
                };
                steps.push(stepObj)
                setControl(prev => ({
                    ...prev,
                    steps: steps
                }));
            } else if ("stateChanges" in step) {
                let stepObj = {
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
            else {
                let stepObj = {
                    python: step.python,
                };
                steps.push(stepObj)
                setControl(prev => ({
                    ...prev,
                    steps: steps
                }));
            }
        })

    }

    const submitAnswer = () => {
        if (mazeData.levelType === 'value_match') {
            const text_answer = document.getElementById("coinsweeper-answer").value;
            fetch('http://localhost:5000/submitAnswer', {
                crossDomain: true,
                method: 'POST',
                body: JSON.stringify({ text_answer : text_answer }),
                headers: {
                      'Content-type': 'application/json'
                  }
                })
                .then(response => response.json())
                .then(response => {
                    setMazeData(prev => ({
                        ...prev,
                        ...response,
                    }))
                }
            )
        }
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
                parseResponse(response, currState)   
            });
    }

    function getPythonicCode() {
        if(control.pythonicCode !== null)
            return control.pythonicCode.replace(/,/g, '\n');
        else
            return null
    }

    function getOutputValue() {
        let output = control.outputValue.toString();
        //TODO: If someone can make this code better, pls do
        output = output.replace(/,/g, '\n');
        output = output.replace(/\n\n*/g, '\n');
        output = output.replace(/^\s*\n+|\s*\n+$/g, '');
        return output;
    }

    const submitCode = function (e) {
        e.preventDefault();
        getSteps(editorValue, mazeData)
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
    const submitButtonStyle = {
        marginTop: '30px',
        width: '110px',
        marginLeft: mazeData.levelType === 'value_match'
        ? '90px'
        : '65%'
    }

    return (
        <>
            <UiConfigs
                penLoc={mazeData.penLoc}
                onPenChange={setPenState}
                onSizeChange={setEditorFont}
            />

            <div className="game-info">
                <h3>Enter your code here:</h3>
                <div className="input-div">
                    <form onSubmit={submitCode}>
                        <div style={{
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
                                fontSize={editorFont}
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
                <br />
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
                        fontSize={editorFont}
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
                    fontSize={editorFont}
                    readOnly={true}
                    name="python-div"
                    editorProps={{ $blockScrolling: true }}
                />
                <ThemeProvider theme={theme}>
                    <div className="submit-area">
                        {mazeData.levelType === 'value_match' ? <input
                            style = {{
                                marginTop: '30px'
                            }}
                            id = "coinsweeper-answer"
                            placeholder="answer" /> : null}
                        <Button
                                onClick = {submitAnswer}
                                style={submitButtonStyle}
                                type="submit"
                                variant="contained"
                                color="primary"
                                endIcon={<PlayArrowRounded />}
                            >
                                Submit
                            </Button>
                    </div>
                </ThemeProvider>
            </div>
            <div className="controller"></div>
        </>
    );
}
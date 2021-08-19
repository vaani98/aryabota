import React, { useState, useContext } from 'react';
import './styles/uiConfigurations.css';
//BUTTON and DROPDOWN COMPONENTS
import Select from 'react-select';
import Button from '@material-ui/core/Button';
//COLOUR PICKER
import { GithubPicker } from 'react-color';
//MATERIAL UI ICONS FOR CONFIG BUTTONS
import PaletteTwoTone from '@material-ui/icons/PaletteTwoTone';
import FormatSize from '@material-ui/icons/FormatSize';
import Translate from '@material-ui/icons/Translate';
import Refresh from '@material-ui/icons/Refresh';
//MAZE STATE
import { MazeState } from './globalStates';
//UTILS
import { convertToContinuousNumbering } from './utils';

/**
 * UI Configuration Toolbar Component
 * This component provides support for:
 * 1. Adjusting font size (s/m/l) ranges
 * 2. Changing webpage base colour
 * 3. Toggling levels
 * @component
 * @example
 * <UiConfigs />
 */
function UiConfigs(props) {

    /**
     * Global context / state to manipulate character location, etc.
     * @const
     */
    const [mazeData, setMazeData] = useContext(MazeState);

    /**
     * color sets the base color of the webpage
     * @var
     */
    let [color, setColor] = useState("");

    /**
     * sizes sets the size range of the text
     * @var
     */
    let [sizes, setSizes] = useState("Medium");

    /**
     * sizes sets the size range of the text
     * @var
     */
    let [level, setLevel] = useState("Go Home");

    /**
     * lang sets the language of the application
     * @var
     */
    let [lang, setLang] = useState("English");

    /**
     * Updates color
     * @param {*} e 
     */
    var colorChange = e => {
        setColor(e.hex);
    }

    /**
     * Updates sizes
     * @param {*} e 
     */
    var sizeChange = e => {
        setSizes(e.label);
        props.onSizeChange(e.editor);
    }

    /**
     * Contains option values for fontSize dropdown
     * @var 
     */
    var sizeValues = [
        {
            value: 1,
            label: "Small",
            editor: 12
        },
        {
            value: 2,
            label: "Medium",
            editor: 14
        },
        {
            value: 3,
            label: "Large",
            editor: 16
        }
    ];

    /**
     * Updates sizes
     * @param {*} e 
     */
    var levelChange = e => {
        setLevel(e.label);
        var selectedLevel = e.value;
        fetch('http://localhost:5000/set_problem', {
            crossDomain: true,
            method: 'POST',
            body: JSON.stringify({ level: selectedLevel }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(response => {
            setMazeData(prev => ({
                ...prev,
                rows: response.rows,
                columns: response.columns,
                coinSweeper: convertToContinuousNumbering(response?.row, response?.column, response?.columns),
                coinLoc: response?.coins?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                obstacleLoc: response?.obstacles?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                positionsSeen: response?.trail?.map(trailObj => convertToContinuousNumbering(trailObj?.row, trailObj?.column, response?.columns)),
                currentDirection: response?.dir,
                levelType: response?.type,
                penLoc: [1],
                prevSteps: 1
            }))
        })
    }

    var levels = [
        {
            value: "go_home",
            label: "Go home",
        },
        {
            value: "count_coins",
            label: "Count total coins",
        },
        {
            value: "check_coins",
            label: "Check & pick coins",
        },
        {
            value: "coins_lte",
            label: "Less than 30 coins"
        },
        {
            value: "Level_1_Easy",
            label: "Level 1 - EASY"
        },
        {
            value: "Level_1_Medium",
            label: "Level 1 - MEDIUM"
        },
        {
            value: "shortest_path",
            label: "shortest path home"
        }
    ];

    /**
     * Updates lang
     * @param {*} e 
     */
    var langChange = e => {
        setLang(e.label);
        var selectedLang = e.label;
        fetch('http://localhost:5000/set_language', {
            crossDomain: true,
            method: 'POST',
            body: JSON.stringify({ lang: selectedLang }),
            headers: {
                'Content-type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(response => {
            setMazeData(prev => ({
                ...prev,
                rows: response.rows,
                columns: response.columns,
                coinSweeper: convertToContinuousNumbering(response?.row, response?.column, response?.columns),
                coinLoc: response?.coins?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                obstacleLoc: response?.obstacles?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                positionsSeen: response?.trail?.map(trailObj => convertToContinuousNumbering(trailObj?.row, trailObj?.column, response?.columns)),
                currentDirection: response?.dir,
                levelType: response?.type,
                penLoc: [1],
                prevSteps: 1
            }))
        })
    }

    var langs = [
        {
            value: "english",
            label: "English",
        },
        {
            value: "kannada",
            label: "Kannada",
        },
        {
            value: "kanglish",
            label: "Kanglish",
        }
    ];
    /**
     * calculates colour values for highlights based on the base colour
     * @param {*} col 
     * @param {*} amt 
     * @returns lightened or darkened colour
     */
    function LightenDarkenColor(col, amt) {

        var colorValue = false;

        if (col[0] === "#") {
            col = col.slice(1);
            colorValue = true;
        }

        var num = parseInt(col, 16);

        var r = (num >> 16) + amt;

        if (r > 255) r = 255;
        else if (r < 0) r = 0;

        var b = ((num >> 8) & 0x00FF) + amt;

        if (b > 255) b = 255;
        else if (b < 0) b = 0;

        var g = (num & 0x0000FF) + amt;

        if (g > 255) g = 255;
        else if (g < 0) g = 0;

        return (colorValue ? "#" : "") + String("000000" + (g | (b << 8) | (r << 16)).toString(16)).slice(-6);

    }

    /**
     * This component displays a button on the toolbar
     * @returns ToggleColor component
     * @example
     * <ToggleColor />
     */
    const ToggleColor = () => {
        var [tc, setTc] = useState(false);
        const onClick = () => {
            if (tc === false) setTc(true);
            else setTc(false);
        }

        return (
            <div className="colorSelector">
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                    startIcon={<PaletteTwoTone />}
                >
                    Edit Color
                </Button>
                {tc ?
                    <GithubPicker
                        onChange={colorChange}
                    ></GithubPicker>
                    : null}
            </div>
        )
    }

    /**
     * This component displays a button on the toolbar
     * @returns ToggleSize component
     * @example
     * <ToggleSize />
     */
    const ToggleSize = () => {
        var [ts, setTs] = useState(false);
        const onClick = () => {
            if (ts === false) setTs(true);
            else setTs(false);
        }

        return (
            <div className="sizeSelector">
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                    startIcon={<FormatSize />}
                >
                    Edit Font Size
                </Button>
                {ts ?
                    <Select
                        id="sizeSelector"
                        placeholder={sizes}
                        options={sizeValues}
                        onChange={sizeChange}
                    />
                    : null}
            </div>
        )
    }

    /**
     * This component displays a button on the toolbar
     * @returns TogglePen component
     * @example
     * <TogglePen />
     * <Select
                        id="LevelSelector"
                        options={levels}
                    />
     */
    const ToggleLevel = () => {
        var [tl, setTl] = useState(false);
        const onClick = () => {
            if (tl === false) setTl(true);
            else setTl(false);
        }

        return (
            <div className="levelSelector">
                {/* <form action="http://localhost:5000/set_problem" method="get"> */}
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                // startIcon={<FormatSize />}
                >
                    Level
                </Button>
                {tl ?
                    <Select
                        id="LevelSelector"
                        name="problem"
                        placeholder={level}
                        options={levels}
                        onChange={levelChange}
                    />
                    : null}
                {/* <input type="submit" value="submit"></input> */}
                {/* </form> */}
            </div>
        )
    }

    /**
     * This component displays a button on the toolbar
     * @returns ToggleLang component
     * @example
     * <ToggleLang />
     */
    const ToggleLang = () => {
        var [tlang, setTlang] = useState(false);
        const onClick = () => {
            if (tlang === false) setTlang(true);
            else setTlang(false);
        }

        return (

            <div className="sizeSelector">
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                    startIcon={<Translate />}
                >
                    Language
                </Button>
                {tlang ?
                    <Select
                        id="sizeSelector"
                        placeholder={lang}
                        options={langs}
                        onChange={langChange}
                    />
                    : null}
            </div>
        )
    }

    /**
     * This component displays a reset button on the toolbar
     * @returns ResetButton component
     * @example
     * <ResetButton />
     */
    const ResetButton = () => {
        const onClick = () => {
            fetch('http://localhost:5000/reset', {
                crossDomain: true,
                method: 'POST',
                headers: {
                    'Content-type': 'application/json'
                }
            })
                .then(response => response.json())
                .then(response => {
                    setMazeData(prev => ({
                        ...prev,
                        rows: response.rows,
                        columns: response.columns,
                        coinSweeper: convertToContinuousNumbering(response?.row, response?.column, response?.columns),
                        coinLoc: response?.coins?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                        obstacleLoc: response?.obstacles?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                        positionsSeen: response?.trail?.map(trailObj => convertToContinuousNumbering(trailObj?.row, trailObj?.column, response?.columns)),
                        currentDirection: response?.dir,
                        levelType: response?.type,
                        penLoc: [1],
                        prevSteps: 1
                    }))
                })
        }

        return (
            <div className="resetButton">
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                    startIcon={<Refresh />}
                >
                    Reset
                </Button>
            </div>
        )
    }

    return (
        <div>
            <style>
                {
                    'body { background-color: ' + color + '; color: ' + LightenDarkenColor(color, -85) + ';}'
                    + '.toolbar { background-color: ' + LightenDarkenColor(color, -35) + ';}'
                    + '.output-title {background-color: ' + color + ';}'
                    + (sizes === "Small" ? 'p { font-size: small;} h3 { font-size: large; } .status { font-size: 22px; } textarea { font-size: 13px;}' :
                        sizes === "Medium" ? 'p { font-size: medium;} h3 { font-size: larger; } .status { font-size: 25px; } textarea { font-size: 15px;}' :
                            sizes === "Large" ? 'p { font-size: larger;} h3 { font-size: x-large; } .status { font-size: 30px; } textarea { font-size: 17px;}' :
                                null)

                }
            </style>
            <div className="toolbar" id="toolbar-div">
                <div className="configs">
                    <ResetButton />
                    <ToggleSize />
                    <ToggleColor />
                    <ToggleLevel />
                    <ToggleLang />
                </div>
            </div>
        </div>
    )
}

export default UiConfigs;
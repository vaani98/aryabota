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
import Create from '@material-ui/icons/Create';
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
 * 3. Toggling pen status (up/down)
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
     * penState sets toggles colour trail visibility
     * @var
     */
    let [penState, setPenState] = useState("penDown");

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
     */
    const TogglePen = () => {
        const onClick = () => {
            if (penState === "penDown") {
                setPenState("penUp");
                props.onPenChange("penUp");
            }
            else {
                setPenState("penDown");
                props.onPenChange("penDown");
            }
        }

        return (
            <div className="penToggle">
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                    startIcon={<Create />}
                >
                    {penState === "penUp" ? "Pen Down" : "Pen Up"}
                </Button>
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
                    startIcon={<Refresh/>}
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
                    <TogglePen />
                </div>
            </div>
        </div>
    )
}

export default UiConfigs;
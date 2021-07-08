import React, { useState } from 'react';
//BUTTON and DROPDOWN COMPONENTS
import Select from 'react-select';
import Button from '@material-ui/core/Button';
//COLOUR PICKER
import { GithubPicker } from 'react-color';
//MATERIAL UI ICONS FOR CONFIG BUTTONS
import PaletteTwoTone from '@material-ui/icons/PaletteTwoTone';
import FormatSize from '@material-ui/icons/FormatSize';
import Create from '@material-ui/icons/Create';

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
function UiConfigs() {

    /**
     * color sets the base color of the webpage
     * @var
     */
    var [color, setColor] = useState("");
    /**
     * sizes sets the size range of the text
     * @var
     */
    var [sizes, setSizes] = useState("Medium");
    /**
     * penState sets toggles colour trail visibility
     * @var
     */
    var [penState, setPenState] = useState("yellow");

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
    }

    /**
     * Contains option values for fontSize dropdown
     * @var 
     */
    var sizeValues = [
        {
            value: 1,
            label: "Small"
        },
        {
            value: 2,
            label: "Medium"
        },
        {
            value: 3,
            label: "Large"
        }
    ];

    // let x = 32;
    // let colors = [];
    // if (x <= 50) {
    //     colors.push('testColor');
    // }
    // else {
    //     colors.push('test2');
    // }

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
        // var [tp, setTp] = useState("penDown");
        const onClick = () => {
            if (penState === "yellow") setPenState("white");
            else setPenState("yellow");
        }

        return (
            <div className="penToggle">
                <Button
                    onClick={onClick}
                    variant="contained"
                    color="secondary"
                    startIcon={<Create />}
                >
                    Pen Up/Down
                </Button>
            </div>
        )
    }

    return (
        <div>
            {/* <h1 className={colors}>{x}</h1> */}
            <style>
                {
                    'body { background-color: ' + color + '; color: ' + LightenDarkenColor(color, -85) + ';}'
                    + '.toolbar { background-color: ' + LightenDarkenColor(color, -35) + ';}'
                    // + '.penDown { background-color: ' + LightenDarkenColor(color, -25) + ';}'
                    + '.penDown { background-color: ' + penState + ';}'
                    + (sizes === "Small" ? 'p { font-size: small;} h3 { font-size: large; } .status { font-size: 22px; } textarea { font-size: 13px;}' :
                        sizes === "Medium" ? 'p { font-size: medium;} h3 { font-size: larger; } .status { font-size: 25px; } textarea { font-size: 15px;}' :
                            sizes === "Large" ? 'p { font-size: larger;} h3 { font-size: x-large; } .status { font-size: 30px; } textarea { font-size: 17px;}' :
                                null)

                }
            </style>
            <div className="toolbar" id="toolbar-div">
                <ToggleSize />
                <ToggleColor />
                <TogglePen />
            </div>
        </div>
    )
}

export default UiConfigs;
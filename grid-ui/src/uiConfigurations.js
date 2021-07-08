import React, { useState } from 'react';
import Select from 'react-select';
import { GithubPicker } from 'react-color';
import Button from '@material-ui/core/Button';
import PaletteTwoTone from '@material-ui/icons/PaletteTwoTone';
import FormatSize from '@material-ui/icons/FormatSize';
import Create from '@material-ui/icons/Create';


function UiConfigs() {

    var [color, setColor] = useState("");
    var [sizes, setSizes] = useState("Medium");
    var [penState, setPenState] = useState("yellow");

    var colorChange = e => {
        setColor(e.hex);
    }

    var sizeChange = e => {
        setSizes(e.label);
    }

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
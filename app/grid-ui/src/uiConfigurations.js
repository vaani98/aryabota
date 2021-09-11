import React, { useState, useContext } from 'react';
import { useHistory } from 'react-router-dom';
import { GoogleLogout } from 'react-google-login';
import './styles/uiConfigurations.css';
//BUTTON and DROPDOWN COMPONENTS
import Select from 'react-select';
import Button from '@material-ui/core/Button';
//COLOUR PICKER
import { GithubPicker } from 'react-color';
//MATERIAL UI ICONS FOR CONFIG BUTTONS
import PaletteTwoTone from '@material-ui/icons/PaletteTwoTone';
import FormatSize from '@material-ui/icons/FormatSize';
import Refresh from '@material-ui/icons/Refresh';
import CodeIcon from '@material-ui/icons/Code';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';
// import LogoutTwoToneIcon from '@mui/icons-material/LogoutTwoTone';
//MAZE STATE
import { MazeState, Constants } from './globalStates';
//UTILS
import { convertToContinuousNumbering } from './utils';
import pes_logo_white_text from './assets/pes_logo_white_text.png';


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

                    startIcon={<PaletteTwoTone />}
                >
                    Color
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

                    startIcon={<FormatSize />}
                >
                    Font Size
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
     * @returns TogglePane component
     * @example
     * <TogglePane />
     */
    const TogglePane = () => {
        var [tp, setTp] = useState(true);
        const onClick = () => {

            if (tp === false) {
                setTp(true);
                document.getElementById("python-pane").style.display = "block";
                document.getElementById("separator-2").style.display = "block";
            }
            else {
                setTp(false);
                document.getElementById("python-pane").style.display = "none";
                document.getElementById("separator-2").style.display = "none";
            }
        }

        return (
            <div className="pythonViewer">
                <Button
                    onClick={onClick}
                    variant="contained"
                    startIcon={<CodeIcon />}
                >
                    Show Python
                </Button>
            </div>
        )
    }

    const InfoButton = () => {
        const history = useHistory();
        const onClick = () => {
            let path = 'home';
            history.push(path);
            console.log('pushed history: ', history);
        }

        return (
            <div className="pythonViewer">
                <InfoOutlinedIcon
                    onClick={onClick}
                />
            </div>
        )
    }

    const LogoutButton = () => {
        const history = useHistory();
        console.log('history: ', history);

        const logout = (response) => {
            console.log("logged out:", response);
            let path = '/';
            history.push(path);
            console.log('pushed history: ', history);
        }

        return (
            <GoogleLogout
                render={renderProps => (
                    <Button variant="contained" startIcon={<CodeIcon />} onClick={renderProps.onClick} disabled={renderProps.disabled}>Logout</Button>
                )}
                clientId={Constants.clientId}
                buttonText="Logout"
                onLogoutSuccess={logout}
            />
        )
    }

    const GridButton = () => {
        const history = useHistory();
        console.log('history: ', history);

        const about = (response) => {
            console.log("about:", response);
            let path = 'grid';
            history.push(path);
            console.log('pushed history: ', history);
        }

        return (
            <Button
                onClick={about}
                variant="contained"
                startIcon="?"
            >
                Grid
            </Button>
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
                        home: response?.homes?.map(obj => convertToContinuousNumbering(obj?.position?.row, obj?.position?.column, response?.columns)),
                        statement: response?.statement,
                        problemSpec: response?.problem_spec,
                        prevSteps: 1
                    }))
                })
        }

        return (
            <div className="resetButton">
                <Button
                    onClick={onClick}
                    variant="contained"

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
                    <img className="pes-logo" alt="PES University Logo" src={pes_logo_white_text} height="45px" />
                    {/* <GridButton /> */}
                    {/* <AboutButton /> */}
                    <ResetButton />
                    <ToggleSize />
                    <ToggleColor />
                    <TogglePane />
                    <InfoButton />
                    <LogoutButton />
                </div>
            </div>
        </div>
    )
}

export default UiConfigs;

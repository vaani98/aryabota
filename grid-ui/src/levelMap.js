import React, { useState, useContext } from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";
import About from './pages/about';
import { Game } from './index';
import './styles/levelMap.css';

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
function LevelMap(props) {
    let [visible, setVisible] = useState("levelMap");

    // var toggleVisibility = () => {
    //     if (visible === "hide") {
    //         setVisible("levelMap");
    //     }
    //     else {
    //         setVisible("hide");
    //     }
    // }

    return (
        <>
            {/* <p onClick={toggleVisibility}>HELLO</p> */}
            <div className={visible}>
                <p>HELLO</p>
                <Router className="router">
                    <Link className="router" to="/">Home</Link>
                    <Link className="router" to="/about">About</Link>
                    <Switch>
                        <Route path="/about">
                            <About />
                        </Route>
                        <Route path="/">
                            {/* <Game /> */}
                        </Route>
                    </Switch>
                </Router>
            </div>
        </>
    );
}

export default LevelMap;
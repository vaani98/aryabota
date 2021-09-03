import React, { useState, useContext } from 'react';
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
    let [visible, setVisible] = useState("hide");

    var toggleVisibility = () => {
        if (visible === "hide") {
            setVisible("levelMap");
        }
        else {
            setVisible("hide");
        }
    }

    return (
        <>
            <p onClick={toggleVisibility}>HELLO</p>
            <div className={visible}>
                <p onClick={toggleVisibility}>HELLO</p>
                <a href="">1</a>
                <a href="">2</a>
                <a href="">3</a>
                <a href="">4</a>
            </div>
        </>
    );
}

export default LevelMap;
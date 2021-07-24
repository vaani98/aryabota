import React, { useContext } from 'react';
import '../styles/ErrorModal.css';
import { MazeState } from '../globalStates';
import Button from '@material-ui/core/Button';

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
function MessageModal(props) {
    const [mazeData, setMazeData] = useContext(MazeState);
    return (
        <div className="modal">
            <div className="modal-content">
                <p style={{
                    marginBottom: '20px'
                }}>{props.error_message}</p>
                <Button 
                    variant="contained"
                    color="secondary"
                    onClick={() => {
                        setMazeData(prev => ({
                            ...prev,
                            error_message: null,
                            message: null,
                            succeeded: null,
                        }))
                }}>OK</Button>
            </div>
        </div>
    )
}

export default MessageModal;
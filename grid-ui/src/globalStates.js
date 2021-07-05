import React from 'react';

/**
 * Global context / state to shared by all the components
 * @exports
 */
export const MazeState = React.createContext([{}, () => {}]);
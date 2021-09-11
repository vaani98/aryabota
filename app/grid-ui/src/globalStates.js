import React from 'react';

/**
 * Global context / state to shared by all the components
 * @exports
 */
export const MazeState = React.createContext([{}, () => {}]);
export const Constants = {
    informationMessage: 'Welcome! We hope you enjoyed learning with AryaBota. To join our discord server, go to https://discord.gg/nEHKaXBn!'
};
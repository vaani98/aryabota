## Iteration 1: BotZero (command line tool)
*BotZero* is a robot in a grid. Its position is defined by its coordinates as in a Cartesian plane. The direction it is facing can be `left`, `right`, `up` or `down`.  

Initial position: `0, 0, up`

For this iteration, we will assume that the grid does not have any obstacles or walls - it's just the Cartesian plane.

### Commands
1. `My X`: What is the bot's x-coordinate?
2. `My Y`: What is the bot's y-coordinate?
3. `Move 10`: Move the bot 10 steps in the direction it is facing.
4. `Turn left`: Turn the bot towards its left (by 90 degrees).
5. `Exit`: Exit the program.

## Iteration 2: CoinSweeper v1 (web app)

Initial position: `0, 0, left`  

Same environment as with *BotZero*, except in a web application. 
Three Panes:
1. Code editor: pseudo-code can be written here and run
2. Python intermediate code: pseudo-code is converted to Python intermediate code and displayed here
3. Visual: visualization of grid with the *CoinSweeper* bot

The command set remains the same as with *BotZero*, except the `Exit` command which is not required anymore.
/**
 * function to generate uniquely random locations for 
 * coins in the given maze.
 * STEP 1: set number of coins as average of number of rows and columns 
 * STEP 2: generate random locations for coin while excluding
 *         robot location (excludePos)
 * @returns [list] coinPositions
 */
 export function randomPositions(columns, rows, excludePos) {
  let coinPositions = [];
  //set number of coins as average of maze size
  const numberOfCoins = Math.floor((columns + columns)/2);
  //generate unique random coin locations by excluding robot location (excludePos)
  while (coinPositions.length < numberOfCoins){
      let x = Math.floor(Math.random() * (columns * columns)) + 1;
      if(coinPositions.indexOf(x) === -1 && !(excludePos === x)) coinPositions.push(x);
  }
  return coinPositions;
}
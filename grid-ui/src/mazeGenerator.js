import React from 'react';
//IMPORT SPRITES
import food_img from './assets/food.svg';
import mario_img from './assets/mario.svg';

/**
 * Component to draw dynamic maze, food and 
 * character based on input
 * This component:
 * 1. take maze size input
 * 2. generate a 2 array of blocks
 * 3. each blocks is returned by Block component
 * 4. send respective food and player sprites to blocks
 * @component
 * @example
 * <Maze x={input.x} y={input.y} foodLoc={mazeData.randomFoods} marioLoc={mazeData.marioLoc} />
 */
export default function Maze(props) {
  /**
   * status/title for maze game
   * @const
   */
  const status = 'MAZE RUNNER';

  /**
   * addRows function to generate a array of row 
   * each containing blocks column in it
   * NOTE: COLUMN REQUIRE ROW ID TO NUMBER EACH BLOCK 
   * @public 
   */
  const addRows = () =>{
    let rows = [];
    for(let i=0; i<props.y; i++){
      rows.push(<div className="maze-row">{addColumn(i)}</div>);
    }
    return rows;
  }

  /**
   * addColumn function to generate a array of column 
   * each containing single block in it
   * NOTE: BLOCK REQUIRE ID (1,2,3...) WE GENERATE ID 
   * FOR EACH BLOCK, SO THAT 10*10 MAZE HAVE 1 TO 100 
   * NUMBERING/ID FOR EACH BLOCK. 
   * @public 
   */
  const addColumn = (row) => {
    let column = [];
    for(let i=0; i<props.x; i++ ){
      //generate id with row number, current column number and a constant
      column.push(renderBlock(props.x*row + (i + 1)));
    }
    return column;
  }

  /**
   * function to render block and set player and food image
   * accordingly.
   * STEP 1: check if current block id match to food location
   *         if so, then set pass food image
   * STEP 2: check if current block id match to player location
   *         if so, then set pass player image
   * STEP 3: else set none to image parameter
   * @param {number} blockCount unique id for each block
   */
  const renderBlock = (blockCount)=> {

    if(props.foodLoc.indexOf(blockCount) !== -1){
      return <Block value={blockCount} image={`url(${food_img})`} />;
    }else if(props.marioLoc === blockCount){
      return <Block value={blockCount} image={`url(${mario_img})`} />;
    }else{
      return <Block value={blockCount} image={'none'} />;
    }

  }  

  return (
    <div>
      <div className="status">{status}</div>
      {addRows()}
    </div>
  );
}


/**
 * Component to draw each block(of maze) with image if any
 * This component:
 * 1. takes image url or none as parameter from mazeGenerator
 * 2. style background image correctly
 * 3. return button with correct and image style
 * @component
 * @example
 * <Block value={blockCount} image={`url(${food_img})`} />
 */
function Block(props) {

  //background image style
  var blockStyle = {
    backgroundSize: "20px",
    backgroundRepeat  : 'no-repeat',
    backgroundPosition: 'center',
    backgroundImage: props.image
  };
  
  return <button style={ blockStyle } className="block" id={"block_" + props.value}>
  </button>;
}
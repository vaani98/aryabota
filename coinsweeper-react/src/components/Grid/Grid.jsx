import React, {useState, useRef} from 'react';
import LineChart from '../LineChart/LineChart';
import robot_down from '../../assets/robot_down.png';
import robot_up from '../../assets/robot_up.png';
import robot_left from '../../assets/robot_left.png';
import robot_right from '../../assets/robot_right.png';
import {getChartJSData, getChartJSOptions} from '../../Utils'
import './Grid.css';

const myImage_right = new Image(50, 50); 
myImage_right.src = robot_right;
const myImage_left = new Image(50, 50); 
myImage_left.src = robot_left;
const myImage_up = new Image(50, 50); 
myImage_up.src = robot_up;
const myImage_down = new Image(50, 50); 
myImage_down.src = robot_down;

const directions = {
  'up': myImage_up,
  'down': myImage_down,
  'left': myImage_left,
  'right': myImage_right,
}

function Grid(props) {
    const all_coordinates = []
    const all_python_commands = []
    props.response_data.map(obj => all_coordinates.push(obj.stateChanges[0]))
    props.response_data.map(obj => all_python_commands.push(obj.python))
    console.log(props.response_data);
    const [data1, setData1] = useState([{
        x: 0,
        y: 0,
    }]);

    const [pointStyle, setPointStyle] = useState([directions[all_coordinates[0].dir]]);
    const index = useRef(0);

    let data = getChartJSData();
    data.datasets[0].data = data1;
    data.datasets[0].pointStyle = pointStyle;
  
    let options = getChartJSOptions();

    const clicky = () => {
        if(index.current === all_coordinates.length) {
            return;
        }
        const temp_pointStyle = pointStyle;

        if(data1[data1.length - 1].x  === all_coordinates[index.current].x 
        && data1[data1.length - 1].y === all_coordinates[index.current].y) {
            temp_pointStyle[pointStyle.length-1] = directions[all_coordinates[index.current].dir];
            setPointStyle([...temp_pointStyle]);
        }
        else {
            temp_pointStyle[temp_pointStyle.length-1] = 'circle'
            setPointStyle([...temp_pointStyle, directions[all_coordinates[index.current].dir]]);
            setData1([...data1, all_coordinates[index.current]]);
        }
        index.current+=1;
    }

  return (
    <div className="grid">
        <button onClick={clicky}> change data </button>
        <pre className="python">{index.current>0 ? all_python_commands[index.current-1] : 'Python commands'}</pre>
        <div className="pre-flex">
            <LineChart height={400} width={400} data={data} options={options} pointStyle={pointStyle}/>
        </div>
    </div>
  );
}

export default Grid;
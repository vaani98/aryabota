import './App.css';
import Grid from './components/Grid/Grid';
import TextArea from './components/TextArea/TextArea';
import React, {useEffect, useState} from 'react';
// import PythonDiv from './components/PythonDiv/PythonDiv';

function App() {
    let responseText ='';
    const sendData = text => {
      console.log(text);
        // fetch('http://localhost:5000/coinSweeper/', {
        //     method: 'POST',
        //     body: JSON.stringify(text),
        //     headers: {
        //         'Content-type': 'application/json'
        //     }
        // })
        // .then(response => response.json())
        // .then(json => {
        //     console.log(json);
        // });
        return [
          {
            "python": "move(2)",
            "stateChanges": [
              {
                "x": 0,
                "y": 3,
                "dir": "left"
              }
            ]
          },
          {
            "python": "turnLeft()",
            "stateChanges": [
              {
                "x": 0,
                "y": 3,
                "dir": "up"
              }
            ]
          },
          {
            "python": "move(6)",
            "stateChanges": [
              {
                "x": 6,
                "y": 3,
                "dir": "up"
              }
            ]
          }
        ]
      
  }
  // setResponseText(sendData('text'));
  responseText = sendData('text');
  return (
    <div className="App">
        <TextArea sendData={sendData} />
        <Grid response_data={responseText}/>
    </div>
  );
}

export default App;

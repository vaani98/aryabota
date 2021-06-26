import React from 'react';

const TextArea = (props) => {
    const postData = () => {
        const text = document.getElementById("hedyCommands").value;
        props.sendData(text);
    }
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            marginRight: '50px'
        }}>
            <textarea id = "hedyCommands" rows="20" cols="50" />
            <button style={{
                width: '100px',
                alignSelf: 'center',
                marginTop: '20px'
            }} onClick={postData}>I'm done!</button>
        </div>
    );
  };
  
  export default TextArea;
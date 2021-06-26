import React from 'react';

const PythonDiv = props => {
    return (
      <pre>
          {props.response_data}
      </pre>
    );
  };
  
  export default PythonDiv;
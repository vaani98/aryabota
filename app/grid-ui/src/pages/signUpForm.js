import React from 'react';
import '../styles/signUpForm.css';
import { TOP_LEVEL_PATHS } from '../constants/routeConstants';
import { useHistory } from 'react-router';
import { useSelector } from 'react-redux';
import { useFormik } from 'formik';

const SignupForm = () => {
  // Pass the useFormik() hook initial form values and a submit function that will
  // be called when the form is submitted
  const history = useHistory();
  const userEmail = useSelector((state) => state.user.email)

  const registerUser = values => {
    // event.preventDefault();
    console.log('!! values', values);
    // var formData = new FormData(document.getElementById('sign-up-form'))
    fetch('http://localhost:5000/api/user', {
        crossDomain: true,
        method: 'POST',
        body: JSON.stringify({email: userEmail}),
        headers: {
            'Content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(response => {
            console.log('!! response form', response);
            // if(response) {
                let path = TOP_LEVEL_PATHS.HOME;
                history.push(path);
                console.log('pushed history: ', history);        
            // }
        });
    }

  
  const formik = useFormik({
    initialValues: {
      firstName: '',
    //   lastName: '',
    },
    onSubmit: values => {
      registerUser(values)
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
        <ul>
            <li>
        <label htmlFor="firstName">Email Address</label>
      <input
        id="firstName"
        name="firstName"
        onChange={formik.handleChange}
        className="field-divided"
        value={formik.values.firstName}
      />
    </li>
        </ul>
      <button type="submit">Submit</button>
    </form>
  );
};

export default SignupForm;
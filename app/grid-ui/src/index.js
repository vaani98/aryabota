import ReactDOM from 'react-dom';
import {
	BrowserRouter as Router,
	Switch,
	Route,
	Link,
	useHistory
} from "react-router-dom";
import { GoogleLogin, GoogleLogout } from 'react-google-login';
import './styles/index.css';
import React, { useState, useLayoutEffect } from 'react';
import About from './about';
import { Game } from './grid';
// Constants
import { Constants } from './globalStates';

const failed = (response) => {
	console.log("failed:", response);
}

const LoginButton = () => {
	const history = useHistory();
	console.log('history: ', history);

	const routeChange = (response) => {
		console.log("success:", response);
		let path = 'home';
		history.push(path);
		console.log('pushed history: ', history);
	}

	return (
		<GoogleLogin
			clientId={Constants.clientId}
			buttonText="Sign In With Google"
			onSuccess={routeChange}
			onFailure={failed}
		/>
	)
}


ReactDOM.render(
	<Router className="router">
		<Switch>
			<Route path="/home">
				<Link className="router" to="/grid">Game</Link>
				<About />
				{/* <LogoutButton /> */}
			</Route>
			<Route path="/grid">
				<Link className="router" to="/home">Home</Link>
				<Game />
				{/* <LogoutButton /> */}
			</Route>
			<Route path="/">
				<LoginButton />
				<ul>
					<li><Link className="router" to="/home">Home</Link></li>
					<li><Link className="router" to="/grid">Game</Link></li>
					<li><Link className="router" to="/">Login/Signup</Link></li>
				</ul>
			</Route>
		</Switch>
	</Router>
	, document.getElementById('root')
);

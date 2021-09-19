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
import bot_img from './assets/bot3.png';
import pes_logo from './assets/pes_logo.png';
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

const Content = () => {
	return (
		<div className="login-content">
			<div style={{ display: "flex", flexDirection: "row" }}>
				<img height="100px" src={pes_logo} />
				<img height="100px" src={bot_img} />
			</div>
			<div>
				<br />
				Hello, welcome to AryaBota!
			</div>
			<div>
				<br />
				We hope you enjoy the experience, and learn programming.
				{/* <ul>
					<li><Link className="router" to="/home">Home</Link></li>
					<li><Link className="router" to="/grid">Game</Link></li>
				</ul> */}
			</div>
			<div className="google-login">
				<br /><br />
				To use the tool, please sign in here:
				<br /><br />
			</div>
			<div>
				<LoginButton />
			</div>

		</div>
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
				{/* <LoginButton /> */}
				<Content />
			</Route>
		</Switch>
	</Router>
	, document.getElementById('root')
);

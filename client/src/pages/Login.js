import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Redirect } from "react-router-dom";
import axios from "axios";

@inject("store")
@observer
export default class Login extends Component {
	constructor(props) {
		super(props);
    this.state = {
      username: '',
      password: ''
    };
	}

	onSubmit(event) {
		const port = 8000;
		axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
		const mutation = this.postLogin(this.state.username, this.state.password);
		axios.post('/graphql/',
			{
				query: mutation,
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
				},
			}
	  )
	  .then(function (response) {
	    console.log(response.data.data.login);
	  })
	  .catch(function (error) {
	    console.log(error);
	  });
	}

	postLogin(username, password) {
		return `mutation { login ( username: "${username}", password: "${password}") {status} }`;
	}

	registerUser() {
		return `mutation { createUser ( username: "${username}", email: "${email}", password: "${password}") { status } }`;
	}

	whoami() {
		const port = 8000;
		axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
		axios.post('/graphql/',
			{
				query: "query{me}",
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
				},
			}
	  )
	  .then(function (response) {
	    console.log(response);
	  })
	  .catch(function (error) {
	    console.log(error);
	  });
	}

	handleUserNameChaned = (e) => {
		this.setState({username: e.currentTarget.value});
	}

	handlePasswordChaned = (e) => {
		this.setState({password: e.currentTarget.value});
	}

	render() {
		return (
			<div className="page login">
				<main>
					<div className='login-window'>
						<div className='login-inputs'>
							<input type="text" placeholder="username"/>
						</div>
						<div className='login-inputs'>
							<input type="password" placeholder="password"/>
						</div>
						<div className='login-button-row'>
							<button type="button"
								className='login-button'
								onClick={this.onSubmit.bind(this)}>
								Login
							</button>
        			<a href='/register'
        				className='button'>
								<button type="button"
									className='login-button'>
									Register
								</button>
							</a>
						</div>

						{this.props.store.authenticated &&
							!this.props.store.authenticating &&
							<Redirect to="/" />}
					</div>
				</main>
				<button type="button"
					className='login-button'
					onClick={this.whoami.bind(this)}>
					whoami
				</button>
			</div>
		);
	}
}

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
      team: '',
      password: '',
      isLoginError: false,
      errorMessage: 'Error'
    };
	}

	onSubmit(event) {
		const port = 8000;
		axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
		const mutation = this.postLogin();
		axios.post('/graphql/',
			{
				query: mutation,
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
				},
			}
	  )
	  .then((response) => {
	    console.log(response);

	    if (response) {

	    } else {
	    	this.setState({
	    		isLoginError: true,
	    		errorMessage: response
	    	});
	    }
	  })
	}

	postLogin() {
		return `mutation { login ( username: "${this.state.team}", password: "${this.state.password}") {status} }`;
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
	handleTeamNameChaned = (e) => {
		this.setState({team: e.currentTarget.value});
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
							<input type="text"
								placeholder="team name"
								onChange={this.handleTeamNameChaned}/>
						</div>
						<div className='login-inputs'>
							<input type="password"
								placeholder="password"
								onChange={this.handlePasswordChaned}/>
						</div>
						{this.state.isLoginError && <div className='error-message'>
							{this.state.errorMessage}
						</div>}
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

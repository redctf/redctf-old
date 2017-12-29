import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import axios from "axios";

@inject("store")
@observer
export default class Login extends Component {
	constructor(props) {
		super(props);
    this.state = {
    	redirectToReferrer: false,
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
	   	const res = response.data;

	    if (res.data.login !== null) {
	    	this.props.store.appState.authenticate(this.state.team).then(() => {
	    		this.props.history.push('/');
	    	});
	    } else {
	    	this.setState({
	    		isLoginError: true,
	    		errorMessage: res.errors[0].message
	    	});
	    }
	  })
	}

	postLogin() {
		return `mutation { login ( username: "${this.state.team}", password: "${this.state.password}") {id} }`;
	}

	handleTeamNameChaned = (e) => {
		this.setState({
			team: e.currentTarget.value,
			isLoginError: false
		});
	}

	handlePasswordChaned = (e) => {
		this.setState({
			password: e.currentTarget.value,
			isLoginError: false
		});
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
					</div>
				</main>
			</div>
		);
	}
}

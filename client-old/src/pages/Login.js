import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import axios from "axios";

@inject("store")
@observer
export default class Login extends Component {
	constructor(props) {
		super(props);
    this.state = {
      username: '',
      password: '',
      isLoginError: false,
      errorMessage: 'Error'
    };
    this.handleKeyPress = ::this.handleKeyPress;
	}

  getTeamInfo() {
	axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
    axios.defaults.withCredentials = true;
    const query = this.queryTeam();
    axios.post('/graphql/',
      {
        query: query,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      }
    )
    .then((response) => {
      console.log('team information:', response);
      this.props.store.appState.team = response.data.data.team;
    })
  }

  queryTeam() {
    return `query { team {id name token points users {id username}}}`;
  }

	onSubmit() {
		if (this.state.username !== '' && this.state.password !== '') {
			axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
			axios.defaults.withCredentials = true;
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
		    	this.props.store.appState.isSuperuser = res.data.login.isSuperuser;
					this.getTeamInfo();

		    	this.props.store.appState.authenticate().then(() => {
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
	}

	postLogin() {
		return `mutation { login ( username: "${this.state.username}", password: "${this.state.password}") {id isSuperuser} }`;
	}

	handleUsernameChanged = (e) => {
		this.setState({
			username: e.currentTarget.value,
			isLoginError: false
		});
	}

	handlePasswordChaned = (e) => {
		this.setState({
			password: e.currentTarget.value,
			isLoginError: false
		});
	}

  handleKeyPress(event) {
    if (event.key === 'Enter' && this.state.username !== '' && this.state.password !== '') {
      this.onSubmit();
    }
  }

	render() {
		const loginDisabled = (this.state.username !== '' && this.state.password !== '') ? '' : 'disabled';
		return (
			<div className="page login">
				<form onKeyPress={this.handleKeyPress}>
					<div className='login-window'>
						<div className='login-inputs'>
							<input type="text"
								className="form-control"
								placeholder="Username"
								onChange={this.handleUsernameChanged}/>
						</div>
						<div className='login-inputs'>
							<input type="password"
								className="form-control"
								placeholder="Password"
								onChange={this.handlePasswordChaned}/>
						</div>
						{this.state.isLoginError && <div className='error-message'>
							{this.state.errorMessage}
						</div>}
						<div className='login-button-row'>
							<button type="button"
								className={`login-button ${loginDisabled}`}
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
				</form>
			</div>
		);
	}
}

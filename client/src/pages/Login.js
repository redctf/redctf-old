import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import axios from "axios";

/* Horizon */
import Horizon from '@horizon/client';

const base_location = document.location.host.split(':')[0];
//const horizon = new Horizon({host: `${location}:8181`});
const horizon = new Horizon({host: `${base_location}`});


const ctf_collection = horizon('ctfs');
const users_collection = horizon('users');
const categories_collection = horizon('categories');
const challenges_collection = horizon('challenges');
const teams_collection = horizon('teams');
const containers_collection = horizon('containers');

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
					// Try moving horizon loads here


					ctf_collection.order('id').watch().subscribe(allCtfs => {
						console.log({horizon_ctf: allCtfs}),
						error => console.error(error);
						this.props.store.appState.ctfs = allCtfs;
					});
					users_collection.order('id').watch().subscribe(allItems => {
						console.log({horizon_users: allItems}),
						error => console.error(error) 
					});
					categories_collection.order('id').watch().subscribe(allCategories => {
						allCategories.sort(function(a,b){return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0); } );
						console.log({horizon_categories: allCategories}), error => console.error(error);
						this.props.store.appState.categories = allCategories;
					});
					challenges_collection.order('id').watch().subscribe(allChallenges => {
						console.log({horizon_challenges: allChallenges}), error => console.error(error);
						this.props.store.appState.challenges = allChallenges;
					});
					containers_collection.order('id').watch().subscribe(allContainers => {
						console.log({horizon_containers: allContainers}), error => console.error(error);
						this.props.store.appState.containers = allContainers;
					});
					teams_collection.order('id').watch().subscribe(allTeams=> {
						// add asolute 0 in teams
						const teams = allTeams.map((team) => {
							const d = this.props.store.appState.ctfs[0].start;
							if (team.solved.length === 0) {
							team.solved.unshift({
								timestamp: d,    
								points: 0
							});
							}
							return team;
						});

						// primary sort is points
						// secondary sort is the earliest timestamp on the last challenge solve
						// third is simple alphabetic sort
						const sortedTeams = teams.sort((a,b) => {
							return (+(b.points > a.points) || +(b.points === a.points) - 1) ||
							(+(a.solved[a.solved.length-1].timestamp > b.solved[b.solved.length-1].timestamp) || 
							+(a.solved[a.solved.length-1].timestamp === b.solved[b.solved.length-1].timestamp) - 1) ||
							(+(a.name > b.name) || +(a.name === b.name) - 1);
						});

						console.log({horizon_teams: sortedTeams}), error => console.error(error);
						this.props.store.appState.teams = sortedTeams;
					});







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

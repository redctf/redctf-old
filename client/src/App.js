import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, withRouter, Redirect } from 'react-router-dom';
import { inject, observer } from 'mobx-react';
import LazyRoute from 'lazy-route';
import DevTools from 'mobx-react-devtools';
import axios from "axios";

/* Horizon */
import Horizon from '@horizon/client';
const horizon = new Horizon({host: 'localhost:8181'});
const users_collection = horizon('users');
const categories_collection = horizon('categories');
const challenges_collection = horizon('challenges');
const teams_collection = horizon('teams');

/* Components */
import TopBar from './components/TopBar';

@withRouter
@inject('store')
@observer
export default class App extends Component {
	constructor(props) {
		super(props);
		this.store = this.props.store;
	}
	componentDidMount() {
		//this.authenticate();

		horizon.connect();

    horizon.onReady().subscribe(() => {
      console.info('Connected to Horizon server');
    });
 
    horizon.onDisconnected().subscribe(() => {
      console.info('Disconnected from Horizon server');
    });

    users_collection.order('id').watch().subscribe(allItems => {
      console.log({horizon_users: allItems}),
      error => console.error(error)	
    });
    categories_collection.order('id').watch().subscribe(allCategories => {
      allCategories.sort(function(a,b){return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0); } );
      console.log({horizon_categories: allCategories}), error => console.error(error);
      this.store.appState.categories = allCategories;
    });
    challenges_collection.order('id').watch().subscribe(allChallenges => {
      console.log({horizon_challenges: allChallenges}), error => console.error(error);
      this.store.appState.challenges = allChallenges;
    });
    teams_collection.order('id').watch().subscribe(allTeams=> {
	    // add asolute 0 in teams
	    const teams = allTeams.map((team) => {
	    	const d = new Date(1517004800 * 1000)    // TODO ctf.start_time
	    	if (team.solved.length === 0) {
		      team.solved.unshift({
		        time: d,    
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
      this.store.appState.teams = sortedTeams;
    });
    this.getTeamInfo();
	}
	authenticate(e) {
		if (e) e.preventDefault();
		//this.store.appState.authenticate();
	}

  getTeamInfo() {
    const port = 8000;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
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
      this.store.appState.team = response.data.data.team;
    })
  }

  queryTeam() {
    return `query { team {id name points users {id username}}}`;
  }

	render() {
		const {
			authenticated,
			isSuperuser,
			timeToRefresh,
			refreshToken,
			testval
		} = this.store.appState;

		const PrivateRoute = ({ component: Component, ...rest }) => (
			// https://reacttraining.com/react-router/web/example/auth-workflow
		  <Route {...rest} render={props => (
		    this.authenticated ? (
		      <Component {...props}/>
		    ) : (
		      <Redirect to={{
		        pathname: '/login',
		        state: { from: props.location }
		      }}/>
		    )
		  )}/>
		);

		return (
			<div className='wrapper'>
				{/*<DevTools />*/}
				<TopBar />

				<Route
					exact
					path='/login'
					render={props => (
						<LazyRoute {...props} component={import('./pages/Login')} />
					)}
				/>
				<Route
					exact
					path='/register'
					render={props => (
						<LazyRoute {...props} component={import('./pages/Register')} />
					)}
				/>
				<Route
					exact
					path='/'
					render={props => (
						authenticated ? (
							<LazyRoute {...props} component={import('./components/Home')} />
						) : (
							<Redirect to="/login"/>
						)
					)}
				/>
				<Route
					exact
					path='/posts'
					render={props => (
						authenticated ? (
							<LazyRoute {...props} component={import('./pages/SubPage')} />
						) : (
							<Redirect to="/login"/>
						)
					)}
				/>
				<Route
					exact
					path='/admin'
					render={props => (
						(authenticated && isSuperuser) ? (
							<LazyRoute {...props} component={import('./pages/Admin')} />
						) : (
							<Redirect to="/login"/>
						)
					)}
				/>
				<Route
					exact
					path='/challenges'
					render={props => (
						authenticated ? (
							<LazyRoute {...props} component={import('./pages/Challenges')} />
						) : (
							<Redirect to="/login"/>
						)
					)}
				/>
				<Route
					exact
					path='/scoreboard'
					render={props => (
						authenticated ? (
							<LazyRoute {...props} component={import('./pages/Scoreboard')}/>
						) : (
							<Redirect to="/login"/>
						)
					)}
				/>
				<Route
					exact
					path='/team'
					render={props => (
						authenticated ? (
							<LazyRoute {...props} component={import('./pages/Team')}/>
						) : (
							<Redirect to="/login"/>
						)
					)}
				/>

				<footer>
					{testval}
					<a href='https://twitter.com/redctf' target='_blank'>
						@red_ctf
					</a>
					{' '}
					| github:
					{' '}
					<a href='https://github.com/redctf/redctf' target='_blank'>
						redctf
					</a>
				</footer>
			</div>
		);
	}
}

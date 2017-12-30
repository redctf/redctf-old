import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, withRouter, Redirect } from 'react-router-dom';
import { inject, observer } from 'mobx-react';
import LazyRoute from 'lazy-route';
import DevTools from 'mobx-react-devtools';

/* Horizon */
import Horizon from '@horizon/client';
const horizon = new Horizon({host: 'localhost:8181'});
const users_collection = horizon('users');

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

    users_collection.order('id'). atch().subscribe(allItems => {
      console.log({users: allItems}),
      error => console.error(error)	
    });
	}
	authenticate(e) {
		if (e) e.preventDefault();
		//this.store.appState.authenticate();
	}

	render() {
		const {
			authenticated,
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
						authenticated ? (
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
					path='/posts/:id'
					render={props => (
						authenticated ? (
							<LazyRoute {...props} component={import('./pages/SubItem')}/>
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

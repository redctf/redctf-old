import React, { Component } from 'react';
import { Route, Link, withRouter } from 'react-router-dom';
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
		this.authenticate();

		horizon.connect();

    horizon.onReady().subscribe(() => {
      console.info('Connected to Horizon server');
    });
 
    horizon.onDisconnected().subscribe(() => {
      console.info('Disconnected from Horizon server');
    });

    users_collection.order('id').watch().subscribe(allItems => {
      console.log({users: allItems}),
      error => console.error(error)	
    });
	}
	authenticate(e) {
		if (e) e.preventDefault();
		this.store.appState.authenticate();
	}
	render() {
		const {
			authenticated,
			authenticating,
			timeToRefresh,
			refreshToken,
			testval
		} = this.store.appState;
		return (
			<div className='wrapper'>
				{/*<DevTools />*/}
				<TopBar />

				<Route
					exact
					path='/'
					render={props => (
						<LazyRoute {...props} component={import('./components/Home')} />
					)}
				/>
				<Route
					exact
					path='/posts'
					render={props => (
						<LazyRoute {...props} component={import('./pages/SubPage')} />
					)}
				/>
				<Route
					exact
					path='/challenges'
					render={props => (
						<LazyRoute {...props} component={import('./pages/Challenges')} />
					)}
				/>
				<Route
					exact
					path='/scoreboard'
					render={props => (
						<LazyRoute {...props} component={import('./pages/Scoreboard')} />
					)}
				/>
				<Route
					exact
					path='/posts/:id'
					render={props => (
						<LazyRoute {...props} component={import('./pages/SubItem')} />
					)}
				/>
				<Route
					exact
					path='/login'
					render={props => (
						<LazyRoute {...props} component={import('./pages/Login')} />
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

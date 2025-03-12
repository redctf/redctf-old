import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, withRouter, Redirect } from 'react-router-dom';
import { inject, observer } from 'mobx-react';
import LazyRoute from 'lazy-route';
import DevTools from 'mobx-react-devtools';
import axios from "axios";

/* Horizon */
import Horizon from '@horizon/client';

const location = document.location.host.split(':')[0];
//const horizon = new Horizon({host: `${location}:8181`});
const horizon = new Horizon({host: `${location}`});


const ctf_collection = horizon('ctfs');
const users_collection = horizon('users');
const categories_collection = horizon('categories');
const challenges_collection = horizon('challenges');
const teams_collection = horizon('teams');
const containers_collection = horizon('containers');

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
    
    horizon.connect();

    horizon.onReady().subscribe(() => {
      console.info('Connected to Horizon server');
    });
 
    horizon.onDisconnected().subscribe(() => {
      console.info('Disconnected from Horizon server');
    });

  }
  authenticate(e) {
    if (e) e.preventDefault();
    //this.store.appState.authenticate();
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
      this.store.appState.team = response.data.data.team;
    })
  }

  queryTeam() {
    return `query { team {id name token points users {id username}}}`;
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
            authenticated ? (
              <LazyRoute {...props} component={import('./pages/Admin/Admin')} />
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
          path='/instructions'
          render={props => (
            authenticated ? (
              <LazyRoute {...props} component={import('./pages/Instructions')} />
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
          path='/teams'
          render={props => (
            authenticated ? (
              <LazyRoute {...props} component={import('./pages/Team')}/>
            ) : (
              <Redirect to="/login"/>
            )
          )}
        />

        <footer className='footer'>
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

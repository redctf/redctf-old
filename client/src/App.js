import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, Link, withRouter, Redirect } from 'react-router-dom';
import { inject, observer } from 'mobx-react';
import LazyRoute from 'lazy-route';
import DevTools from 'mobx-react-devtools';
import axios from "axios";

/* Horizon */
import Horizon from '@horizon/client';

const location = document.location.host.split(':')[0];
const horizon = new Horizon({host: `${location}:8181`});


const ctf_collection = horizon('ctfs');
const users_collection = horizon('users');
const categories_collection = horizon('categories');
const challenges_collection = horizon('challenges');
const teams_collection = horizon('teams');
const containers_collection = horizon('containers');
const auth_collection = horizon('auth');

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

    //this.getMyInfo();

    const port = 8000;
    axios.defaults.baseURL = `${document.location.protocol}//${document.location.hostname}:${port}`;
    axios.defaults.withCredentials = true;
    const query = `query { me {id isSuperuser username}}`;
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
      console.log('my information inline:', response);
      //this.store.appState.team = response.data.data.team;

      const res = response.data;
      
      if (res.data.me !== null) {
        this.props.store.appState.isSuperuser = res.data.me.isSuperuser;
        this.store.appState.me = res.data.me;

        // this.props.store.appState.authenticate().then(() => {
        //   //this.props.history.push('/');
        // });
      }

    })


    horizon.connect();

    horizon.onReady().subscribe(() => {
      console.info('Connected to Horizon server.');
    });
 
    horizon.onDisconnected().subscribe(() => {
      console.info('Disconnected from Horizon server');
    });

    ctf_collection.order('id').watch().subscribe(allCtfs => {
      console.log({horizon_ctf: allCtfs}),
      error => console.error(error);
      this.store.appState.ctfs = allCtfs;
    })

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
    containers_collection.order('id').watch().subscribe(allContainers => {
      console.log({horizon_containers: allContainers}), error => console.error(error);
      this.store.appState.containers = allContainers;
    });
    teams_collection.order('id').watch().subscribe(allTeams=> {
      // add asolute 0 in teams
      const teams = allTeams.map((team) => {
        const d = this.store.appState.ctfs[0].created;    // TODO ctf.start_time
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
      this.store.appState.teams = sortedTeams;
    });
    this.getTeamInfo();

    //this.authenticate();
  }
  authenticate(e) {
    if (e) e.preventDefault();
    console.log('got to authenticate in App.js')
    //this.getMyInfo();
    //this.store.appState.authenticate();
  }

  getMyInfo() {
    const port = 8000;
    axios.defaults.baseURL = `${document.location.protocol}//${document.location.hostname}:${port}`;
    axios.defaults.withCredentials = true;
    const query = this.queryMe();
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
      console.log('my information:', response);
      //this.store.appState.team = response.data.data.team;

      const res = response.data;
      
      if (res.data.me !== null) {
        this.props.store.appState.isSuperuser = res.data.me.isSuperuser;
        this.store.appState.me = response.data.me;

        // this.props.store.appState.authenticate().then(() => {
        //   //this.props.history.push('/');
        // });
      }

    })
  }

  queryMe() {
    return `query { me {id isSuperuser username}}`;
  }

  getTeamInfo() {
    const port = 8000;
    axios.defaults.baseURL = `${document.location.protocol}//${document.location.hostname}:${port}`;
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

  // requireAuth5() {
  //   console.log('called requireAuth5');
  //   return new Promise((resolve, reject) => {
  //     console.log('returning false');
  //     resolve(false);
  //   });
  // }
  
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
      //console.log('in PrivateRoute: ',this.authenticated);
      //console.log('in PrivateRoute: '),
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
              console.log('testtrue'),<LazyRoute {...props} component={import('./pages/Challenges')} />
            ) : (
              console.log('testfalse'),<Redirect to="/login"/>
            )
          )}
        />
        {/* <Route
          exact
          path='/challenges'
          render={props => (
            requireAuth4().then( res => { return res ? (
              console.log('testtrue'),<LazyRoute {...props} component={import('./pages/Challenges')} />
            ) : (
              console.log('testfalse'),<Redirect to="/login"/>
            ) })
          )}
        /> */}
        {/* <Route
          exact
          path='/challenges'
          render={props => (
            this.requireAuth5().then( res => { return res }) ? (
              console.log('$',this.requireAuth5().then( res => { return res })),console.log('testtrue'),<LazyRoute {...props} component={import('./pages/Challenges')} />
            ) : (
              console.log('testfalse'),<Redirect to="/login"/>
            ) 
          )}
        /> */}
        {/* <Route
          exact
          path='/challenges'
          render={props => (
            this.requireAuth5().then() ? (
              console.log('$',this.requireAuth5()),console.log('testtrue'),<LazyRoute {...props} component={import('./pages/Challenges')} />
            ) : (
              console.log('testfalse'),<Redirect to="/login"/>
            ) 
          )}
        /> */}
        {/* <Route
          exact
          path='/challenges'
          render={props => (
            requireAuth3() === true ? (
              console.log('testtrue'),<LazyRoute {...props} component={import('./pages/Challenges')} />
            ) : (
              console.log('testfalse'),<Redirect to="/instructions"/>
            )
          )}
        /> */}
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
          path='/team'
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

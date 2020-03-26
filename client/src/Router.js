import React from 'react'
import {
  BrowserRouter as Router,
  Route,
  Link,
  Redirect,
  withRouter
} from 'react-router-dom'

import Login from './pages/Login';
import Register from './pages/Register';
import Home from './components/Home';
import Admin from './pages/Admin/Admin';
import Challenges from './pages/Challenges';
import Instructions from './pages/Instructions';
import Scoreboard from './pages/Scoreboard';
import Team from './pages/Team';
import TurtleSoup from './pages/TurtleSoup';
import SpecialThanks from './pages/SpecialThanks';


const fakeAuth = {
  isAuthenticated: false,
  authenticate(cb) {
    this.isAuthenticated = true
    setTimeout(cb, 100)
  },
  signout(cb) {
    this.isAuthenticated = false
    setTimeout(cb, 100)
  }
}

// class Login extends React.Component {
//   state = {
//     redirectToReferrer: false
//   }
//   login = () => {
//     fakeAuth.authenticate(() => {
//       this.setState(() => ({
//         redirectToReferrer: true
//       }))
//     })
//   }
//   render() {
//     const { from } = this.props.location.state || { from: { pathname: '/' } }
//     const { redirectToReferrer } = this.state

//     if (redirectToReferrer === true) {
//       return <Redirect to={from} />
//     }

//     return (
//       <div>
//         <p>You must log in to view the page</p>
//         <button onClick={this.login}>Log in</button>
//       </div>
//     )
//   }
// }

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route {...rest} render={(props) => (
    fakeAuth.isAuthenticated === true
      ? <Component {...props} />
      : <Redirect to={{
          pathname: '/login',
          state: { from: props.location }
        }} />
  )} />
)

// const AuthButton = withRouter(({ history }) => (
//   fakeAuth.isAuthenticated ? (
//     <p>
//       Welcome! <button onClick={() => {
//         fakeAuth.signout(() => history.push('/'))
//       }}>Sign out</button>
//     </p>
//   ) : (
//     <p>You are not logged in.</p>
//   )
// ))

export default function Routes () {
  return (
    <Router>
      <div>
        <Route
          exact
          path='/login'
          component={Login}
        />
        <Route
          exact
          path='/register'
          component={Register}
        />
        <Route
          exact
          path='/'
          component={Home}
        />
        <PrivateRoute
          exact
          path='/admin'
          component={Admin}
        />
        <PrivateRoute
          exact
          path='/challenges'
          component={Challenges}
        />
        <Route
          exact
          path='/instructions'
          component={Instructions}
        />
        <Route
          exact
          path='/scoreboard' 
          component={Scoreboard}
        />
        <Route
          exact
          path='/turtlesoup' 
          component={TurtleSoup}
        />
        <Route
          exact
          path='/special-thanks' 
          component={SpecialThanks}
        />
        <PrivateRoute
          exact
          path='/team'
          component={Team}
        />
      </div>
    </Router>
  )
}
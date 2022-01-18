import React, { useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import './Login.scss';

async function loginUser(credentials) {
  const mut = `mutation {
    login(username: "${credentials.username}", password: "${credentials.password}") {
      id
      token
      username
      isSuperuser
    }
  }`;

  axios.defaults.baseURL = `${window.location.protocol}//${window.location.hostname}`;
  axios.defaults.withCredentials = true;
  const res = await axios.post('/graphql/',
    {
      query: mut,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    }
  );
  console.log('user from loginUser: ', res.data.data.login);
  return res.data.data.login;
}

export default function Login({ setUser }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    const user = await loginUser({
      username,
      password
    });
    setUser(user);
  }

  return (
    <div className="login-wrapper">
      <h1>Please Log In</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>Username</p>
          <input type="text" onChange={e => setUserName(e.target.value)}/>
        </label>
        <label>
          <p>Password</p>
          <input type="password" onChange={e => setPassword(e.target.value)}/>
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
}

Login.propTypes = {
  setUser: PropTypes.func.isRequired
};
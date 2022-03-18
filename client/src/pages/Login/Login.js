import React, { useState } from 'react';
import PropTypes from 'prop-types';
import axiosInstance from '../../axiosApi';
import './Login.scss';

async function loginUser(credentials) {
  const mut = `mutation {
    tokenAuth(username: "${credentials.username}", password: "${credentials.password}") {
      success
      errors
      token
      user {
        username
      }
    }
  }`;

  try {
    const response = await axiosInstance.post('/graphql/', {
      query: mut
    });
    // axiosInstance.defaults.headers.common['Authorization'] = `JWT ${response.data.data.tokenAuth.token}`;
    sessionStorage.setItem('user', JSON.stringify(response.data.data.tokenAuth));

    return response.data.data.tokenAuth;
  } catch (error) {
    throw `Error in Login.js: ${error}`;
  }
}

export default function Login({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();
  const [error, setError] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    const user = await loginUser({
      username,
      password
    });
    setToken(user);
  }

  const loginDisabled = !username || !password;

  return (
    <div className="center-top-wrapper">
      <div className="login-container">
        <form onSubmit={handleSubmit}>
          <div className='login-input'>
            <input type="text"
              value={username}
              className='form-control'
              placeholder='Username' 
              onChange={e => setUserName(e.target.value)}/>
          </div>
          <div className='login-input'>
            <input type="password" 
              value={password}
              className='form-control'
              placeholder='Password' 
            onChange={e => setPassword(e.target.value)}/>
          </div>
          <div className='button-row'>
            <button disabled={loginDisabled} type="submit">Login</button>
            <a href='/register' className='button'>
              <button type="button">Register</button>
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
};
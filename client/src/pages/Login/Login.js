import React, { useState } from 'react';
import { inject, observer } from 'mobx-react';
import PropTypes from 'prop-types';
import axiosInstance from '../../axiosApi';
//import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
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
    axiosInstance.defaults.headers.common['Authorization'] = `JWT ${response.data.data.tokenAuth.token}`;
    sessionStorage.setItem('user', JSON.stringify(response.data.data.tokenAuth));

    return response.data.data.tokenAuth;
  } catch (error) {
    throw `Error in Login.js: ${error}`;
  }



  // axios.defaults.baseURL = `${window.location.protocol}//${window.location.hostname}`;
  // axios.defaults.withCredentials = true;
  // const res = await axios.post('/graphql/', {
  //   query: mut,
  //   headers: {
  //     'Accept': 'application/json',
  //     'Content-Type': 'application/json',
  //   },
  // });

  // console.log('user from loginUser: ', res.data.data.tokenAuth);
  // return res.data.data.tokenAuth;
}

function ErrorStatus(props) {
  return loginUser(props.credentials).then(user => {
    if (user == null) {
      return true;
    }
    return false;
  });
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
  setToken: PropTypes.func.isRequired
};
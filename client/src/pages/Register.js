import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Redirect } from "react-router-dom";
import axios from "axios";

@inject("store")
@observer
export default class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      password: '',
      email: ''
    };
  }

  onSubmit(event) {
    const port = 8000;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
    const mutation = this.registerUser();
    axios.post('/graphql/',
      {
        query: mutation,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      }
    )
    .then(function (response) {
      console.log(response);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

  registerUser() {
    return `mutation { createUser ( username: "${this.state.username}", email: "${this.state.email}", password: "${this.state.password}") { status } }`;
  }

  handleUserNameChaned = (e) => {
    this.setState({username: e.currentTarget.value});
    console.log('this.state.username:', this.state.username);
  }

  handlePasswordChaned = (e) => {
    this.setState({password: e.currentTarget.value});
  }

  handleEmailChaned = (e) => {
    this.setState({email: e.currentTarget.value});
  }

  render() {
    return (
      <div className="page login">
        <main>
          <div className='login-window'>
            <div className='login-inputs'>
              <input type="text"
                placeholder="username"
                onChange={this.handleUserNameChaned}/>
            </div>
            <div className='login-inputs'>
              <input type="password"
                placeholder="password"
                onChange={this.handlePasswordChaned}/>
            </div>
            <div className='login-inputs'>
              <input type="text"
                placeholder="email address"
                onChange={this.handleEmailChaned}/>
            </div>
            <div className='login-button-row'>
              <button type="button"
                className='login-button'
                onClick={this.onSubmit.bind(this)}>
                Register
              </button>
            </div>
          </div>
        </main>
      </div>
    );
  }
}

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
      team: '',
      password: '',
      email: '',
      isRegistrationError: false,
      errorMessage: 'Error',
      isRegistrationSuccess: false,
      successMessage: 'Success'
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
    .then((response) => {
      console.log(response);
      const res = response.data;

      if (res.data.createUser !== null) {
        console.log('success' + res.data.createUser.status);
        this.setState({
          isRegistrationSuccess: true,
          successMessage: res.data.createUser.status
        }, () => {
          setTimeout(() => {
            this.props.history.push('/login');
          }, 200);
        });
      } else {
        this.setState({
          isRegistrationError: true,
          errorMessage: res.errors[0].message
        });
      }
    })
  }

  registerUser() {
    return `mutation { createUser ( username: "${this.state.team}", email: "${this.state.email}", password: "${this.state.password}") { status } }`;
  }

  handleTeamNameChaned = (e) => {
    this.setState({
      team: e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handlePasswordChaned = (e) => {
    this.setState({
      password: e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handleEmailChaned = (e) => {
    this.setState({
      email: e.currentTarget.value,
      isRegistrationError: false
    });
  }

  render() {
    return (
      <div className="page login">
        <main>
          <div className='login-window'>
            <div className='login-inputs'>
              <input type="text"
                placeholder="team name"
                onChange={this.handleTeamNameChaned}/>
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
            {this.state.isRegistrationError && <div className='error-message'>
              {this.state.errorMessage}
            </div>}
            {this.state.isRegistrationSuccess && <div className='success-message'>
              {this.state.successMessage}
            </div>}
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

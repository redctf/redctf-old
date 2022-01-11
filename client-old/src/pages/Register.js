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
      regNewTeam: false,
      regJoinTeam: false,
      team: '',
      username: '',
      token: '',
      password: '',
      passwordConfirmed: '',
      email: '',
      isRegistrationError: false,
      errorMessage: 'Error',
      isRegistrationSuccess: false,
      successMessage: 'Success'
    };
  }

  onSubmit(event) {
    let mutation;
    if (this.state.regNewTeam) {
      mutation  = this.registerTeam();

      axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
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
        const res = response.data;
        console.log(response);

        if (res.data.createTeam !== null) {
          console.log('Team create success:', res.data.createTeam.status);
          let token = res.data.createTeam.token;
          mutation = this.registerUser(token);

          axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
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
              console.log('User create success:', res.data.createUser.status);
              this.setState({
                isRegistrationSuccess: true,
                successMessage: 'User and team created successfully'
              }, () => {
                setTimeout(() => {
                  this.props.history.push('/login');
                }, 3000);
              });
            } else if(res.errors) {
              this.setState({
                isRegistrationError: true,
                errorMessage: res.errors[0].message
              }, () => {
                setTimeout(() => {
                  this.setState({
                    isRegistrationError: false
                  });
                }, 5000);
              });
            }
          })
        } else if(res.errors) {
          this.setState({
            isRegistrationError: true,
            errorMessage: res.errors[0].message
          }, () => {
            setTimeout(() => {
              this.setState({
                isRegistrationError: false
              });
            }, 5000);
          });
        }
      })

    } else {
      mutation  = this.joinTeam();

      axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
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
        const res = response.data;
        console.log(response);

        if (res.data.createUser !== null) {
          console.log('User create success:', res.data.createUser.status);
          this.setState({
            isRegistrationSuccess: true,
            successMessage: 'User created and team joined successfully'
          }, () => {
            setTimeout(() => {
              this.props.history.push('/login');
            }, 3000);
          });
        } else if(res.errors) {
          this.setState({
            isRegistrationError: true,
            errorMessage: res.errors[0].message
          }, () => {
            setTimeout(() => {
              this.setState({
                isRegistrationError: false
              });
            }, 5000);
          });
        }
      })
    }
  }



  onBack(event) {
    this.setState({
      regNewTeam: false,
      regJoinTeam: false,
      regNewTeam: false,
      regJoinTeam: false,
      team: '',
      username: '',
      token: '',
      password: '',
      passwordConfirmed: '',
      email: '',
      isRegistrationError: false,
      errorMessage: 'Error',
      isRegistrationSuccess: false,
      successMessage: 'Success'
    });
  }

  onNewRegistration(event) {
    this.setState({
      regNewTeam: true
    });
  }

  onJoinRegistration(event) {
    this.setState({
      regJoinTeam: true
    });
  }

  onBackSubmit(event) {
    this.props.history.push('/login');
    this.setState({
      regNewTeam: false,
      regJoinTeam: false,
      regNewTeam: false,
      regJoinTeam: false,
      team: '',
      username: '',
      token: '',
      password: '',
      passwordConfirmed: '',
      email: '',
      isRegistrationError: false,
      errorMessage: 'Error',
      isRegistrationSuccess: false,
      successMessage: 'Success'
    });
  }

  registerTeam() {
    return `mutation { createTeam ( teamname: "${this.state.team}", username: "${this.state.username}", email: "${this.state.email}", password: "${this.state.password}", hidden: false) { status, token } }`;
  }
  registerUser(token) {
    return `mutation { createUser ( username: "${this.state.username}", token: "${token}", email: "${this.state.email}", password: "${this.state.password}", hidden: false) { status } }`;
  }
  joinTeam() {
    return `mutation { createUser ( username: "${this.state.username}", token: "${this.state.token}", email: "${this.state.email}", password: "${this.state.password}", hidden: false) { status } }`;
  }

  handleTeamNameChanged = (e) => {
    this.setState({
      team: e.currentTarget.value,
      reqTeam: !!e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handleUsernameChanged = (e) => {
    this.setState({
      username: e.currentTarget.value,
      reqUsername: !!e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handleTokenChanged = (e) => {
    this.setState({
      token: e.currentTarget.value,
      reqToken: !!e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handlePasswordChanged = (e) => {
    this.setState({
      password: e.currentTarget.value,
      reqPassword: !!e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handlePasswordConfirmChanged = (e) => {
    this.setState({
      passwordConfirmed: e.currentTarget.value,
      reqPasswordConf: !!e.currentTarget.value,
      isRegistrationError: false
    });
  }

  handleEmailChanged = (e) => {
    this.setState({
      email: e.currentTarget.value,
      reqEmail: !!e.currentTarget.value,
      isRegistrationError: false
    });
  }

  render() {
    const pwdConfirmed = (this.state.password === this.state.passwordConfirmed && this.state.password !== '') ? true : false;
    const registrationDisabled = (pwdConfirmed && this.state.username !== '' && this.state.email !== '' && (this.state.team !== '' || this.state.token !== '')) ? '' : 'disabled';
    return (
      <div className="page login">
        <main>
          {
            (this.state.regNewTeam || this.state.regJoinTeam) &&
            <div className='login-window'>
              {this.state.regNewTeam &&
                <div className='login-inputs'>
                  <input type="text"
                    className="form-control input-req"
                    placeholder="Team Name"
                    onChange={this.handleTeamNameChanged}/>
                  {!this.state.team && <span className='req-input'>*</span>}
                </div>
              }
              <div className='login-inputs'>
                <input type="text"
                  className="form-control input-req"
                  placeholder="Username"
                  onChange={this.handleUsernameChanged}/>
                  {!this.state.username && <span className='req-input'>*</span>}
              </div>
              {this.state.regJoinTeam &&
                <div className='login-inputs'>
                  <input type="text"
                    className="form-control input-req"
                    placeholder="Token"
                    onChange={this.handleTokenChanged}/>
                  {!this.state.token && <span className='req-input'>*</span>}
                </div>
              }
              <div className='login-inputs'>
                <input type="password"
                  className="form-control input-req"
                  placeholder="Password"
                  onChange={this.handlePasswordChanged}/>
                  {!this.state.password && <span className='req-input'>*</span>}
              </div>
              <div className='login-inputs'>
                <input type="password"
                  className="form-control input-req"
                  placeholder="Confirm Password"
                  onChange={this.handlePasswordConfirmChanged}/>
                  {!this.state.passwordConfirmed && <span className='req-input'>*</span>}
              </div>
              <div className='login-inputs'>
                <input type="text"
                  className="form-control input-req"
                  placeholder="Email Address"
                  onChange={this.handleEmailChanged}/>
                  {!this.state.email && <span className='req-input'>*</span>}
              </div>
              <div>
                  <span className='req-text'>* required</span>
              </div>
              {this.state.isRegistrationError && <div className='error-message'>
                {this.state.errorMessage}
              </div>}
              {this.state.isRegistrationSuccess && <div className='success-message'>
                {this.state.successMessage}
              </div>}
              <div className='login-button-row'>
                <button type="button"
                  className='back-button'
                  onClick={this.onBack.bind(this)}>
                  Back
                </button>
                <button type="button"
                  className={`login-button ${registrationDisabled}`}
                  onClick={this.onSubmit.bind(this)}>
                  Register
                </button>
              </div>
            </div>
          }
          {
            (!this.state.regNewTeam && !this.state.regJoinTeam) &&
            <div className='choose-window'>
              <button type='button'
                className='choose-button choose-new-team'
                onClick={this.onNewRegistration.bind(this)}>
                Register a New Team
              </button>
              <button type='button'
                className='choose-button choose-join-team'
                onClick={this.onJoinRegistration.bind(this)}>
                Register and Join Existing Team
              </button>
              <button type='button'
                className='choose-button choose-back'
                onClick={this.onBackSubmit.bind(this)}>
                Back to Login
              </button>
            </div>
          }
        </main>
      </div>
    );
  }
}

import React, { Component } from "react";
import { inject } from "mobx-react";
import axios from 'axios';

@inject("store")
export default class ChallengeModal extends Component {
  static displayName='ChallengeModal';
  constructor(props) {
    super(props);
    this.store = this.props.store.appState;
    this.state = {
      challenge: {
        flag: ''
      }
    };
  }

  onSubmit(e) {
    //const port = 8000;
    //axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
    const mutation = ''
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
    })
  }

  handleContainerClick = (e) => {
    // Determine if container for click already exists
    const container = this.store.containers.filter((ele) => {
      return ele.challenge === this.props.sid;
    }).filter((ele) => {
      return ele.user === parseInt(this.store.team.id, 10);
    })[0];

    if (container) {
      // if there exists a container for this challenge and this user...

      // create cookie
      const newCookie = `redctf=${container.name.split('_')[1]}`;
      document.cookie = newCookie;

      // redirect to path
      window.location = 'http://'+window.location.hostname+':80/'+this.props.path;
      // window.location = this.props.path;
    } else {
      // container does not exist, must create using graphQL call
      //const port = 8000;
      //axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
      axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
      const mutation = `mutation { getUserContainer ( challengeId: ${this.props.sid}) {status, containerName, nextHop } }`;
    
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
        const result = response.data.data.getUserContainer;
        console.log(result.status);

        // create cookie
        const newCookie = `redctf=${result.containerName.split('_')[1]}`;
        document.cookie = newCookie;

        // redirect to path
        window.location = 'http://'+window.location.hostname+':80/'+result.nextHop;
        // window.location = result.nextHop;
        console.log(result.status);
      })
    }
  }

  handleFieldChanged = (e) => {
    const challenge = {...this.state.challenge};
    challenge[e.currentTarget.id] = e.currentTarget.value;
    this.setState({challenge});
  }

  render() {
    const solveString = this.props.solves ? this.props.solves : 0;
    const solves = solveString === 1 ? `${solveString} Solve` : `${solveString} Solves`;

    // TODO - Render hosted information
    return (
      <div className='challenge-modal'>
        <div className='title-bar'>
          <div className='title'>{this.props.name}</div>
          <div className='points'>{this.props.value} Points</div>
        </div>

        <div className='challenge-modal-content'>
          <div dangerouslySetInnerHTML={{__html: this.props.description}}></div>
    
          {this.props.path && 
            <a className='container-link'
              onClick={this.handleContainerClick}
              target="_blank">Click Here For Container
            </a>
          }

          <div className='footer-bar'>
            <p>{solves}</p>
          </div>
        </div>
      </div>
    );
  }
}

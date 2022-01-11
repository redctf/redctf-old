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
      },
      showSpinner: false,
      launchWording: 'Launch Challenge'
    };
  }

  onSubmit(e) {
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
  handleDownloadClick = (e) => {
    window.open(`${location.protocol}//${location.hostname}${this.props.downloadPath}`,  '_blank');
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
      const hash = container.name.split('_').slice(-1)[0];
      const newCookie = `redctf-${hash}=${hash}`;
      document.cookie = newCookie;

      // redirect to path
      window.open(`${location.protocol}//${location.hostname}/${this.props.path}`,  '_blank');

    } else {
      // container does not exist, must create using graphQL call
      this.setState({
        showSpinner: true,
        launchWording: 'Launching . . .'
      });
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
        const hash = result.containerName.split('_').slice(-1)[0];
        const newCookie = `redctf-${hash}=${hash}`;
        document.cookie = newCookie;

        this.setState({
          showSpinner: false
        });

        // redirect to path
        window.open(`${location.protocol}//${location.hostname}/${result.nextHop}`,  '_blank');
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
    const host = document.location.origin.split(':')[0];

    // TODO - Render hosted information
    return (
      <div className='challenge-modal'>
        <div className='title-bar'>
          <div className='title'>{this.props.name}</div>
          <div className='points'>{this.props.value} Points</div>
        </div>

        <div className='challenge-modal-content'>
          <div dangerouslySetInnerHTML={{__html: this.props.description}}></div>
    
          
          {this.props.hosted &&
            <a className='container-link'
              onClick={this.handleContainerClick}
              target="_blank">{this.state.launchWording}
            </a>
          }
          
          
          {this.props.fileUpload && 
            <a className='container-link'
              onClick={this.handleDownloadClick}
              target="_blank">Download File
            </a>
          }

          {this.state.showSpinner && <div className="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>}

          <div className='footer-bar'>
            <p>{solves}</p>
          </div>
        </div>
      </div>
    );
  }
}

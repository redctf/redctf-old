import React, { Component } from "react";
import { inject } from "mobx-react";

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
    const port = 8000;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
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
    // if (in horizon datastore) container exists for user/challenge combo
    // - use container_name field to parse out shas256 and use sha256 to set redctf cookie
    // - redirect to pathPrefix

    console.log('chalmod props', this.props);
    console.log('chalmod store', this.store);

    const challengeId = this.props.sid;
    const teamId = this.store.team.id;

    const container_exists = true;

    if (container_exists) {



    } else {
      const port = 8000;
      axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
      const mutation = '/getusercontainer/'
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





    // else (no container)
    // - ajax call to create container
    // - take return value of container_name to set cookie
    // - redirect

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

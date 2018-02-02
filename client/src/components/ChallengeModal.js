import React, { Component } from "react";

export default class ChallengeModal extends Component {
  static displayName='ChallengeModal';
  constructor(props) {
    super(props);
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

  handleFieldChanged = (e) => {
    const challenge = {...this.state.challenge};
    challenge[e.currentTarget.id] = e.currentTarget.value;
    this.setState({challenge});
  }

  render() {
    const solveString = this.props.solves ? this.props.solves : 0;
    const solves = solveString === 1 ? `${solveString} Solve` : `${solveString} Solves`;
    return (
      <div className='challenge-modal'>
        <div className='title-bar'>
          <div className='title'>{this.props.name}</div>
          <div className='points'>{this.props.value} Points</div>
        </div>

        <div className='challenge-modal-content'>
          <a href={this.props.description} target="_blank">Click here</a>

          <div className='footer-bar'>
            <p>{solves}</p>
          </div>
        </div>
      </div>
    );
  }
}

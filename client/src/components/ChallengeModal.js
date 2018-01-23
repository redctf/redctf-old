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
    return (
      <div className='challenge-modal'>
        <div className='title-bar'>
          <div className='title'>{this.props.name}</div>
          <div className='points'>{this.props.value} Points</div>
        </div>


        <p>{this.props.description}</p>
      </div>
    );
  }
}

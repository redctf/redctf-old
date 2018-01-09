import React, { Component } from "react";

export default class ChallengeModal extends Component {
  static displayName='ChallengeModal';
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className='challenge-modal'>
        <h2>{this.props.name}</h2>
        <small>{this.props.value} Points</small>
        <p>{this.props.description}</p>
      </div>
    );
  }
}

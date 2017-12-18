import React, { Component } from "react";

export default class ChallengeModal extends Component {
  static displayName='ChallengeModal';
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className='challenge-modal'>
        <p>Challenge Modal</p>
      </div>
    );
  }
}

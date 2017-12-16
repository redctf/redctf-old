import React, { Component } from "react";
import { observer } from "mobx-react";

import ChallengeModal from '../ChallengeModal/ChallengeModal';

export default class JeopardyButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showModal: false
    };
  }
  render () {
    const buttonStyle = {
      backgroundColor: (this.props.solved) ? 'green' : 'blue'
    };
    return (
      <div className='jeopardy-button' style={buttonStyle}>
        <a className='button' onClick={this.handleClick}>{this.props.value}</a>
        <ChallengeModal visible={this.state.showModal}/>
      </div>
    );
  }

  handleClick = () => {
    this.setState({showModal: true});
  }

  hideModal = () => {
    this.setState({showModal: false});
  }

};



  
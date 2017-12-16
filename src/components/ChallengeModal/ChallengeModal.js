import React, { Component } from "react";

import Modal from '../ui/Modal';

export default class ChallengeModal extends Component {
  static propTypes = {
    visible: React.PropTypes.bool
  };
  render() {
    console.log('gets to the modal ' + this.props.visible);
    return (
      <div>
        <Modal width={600}
          visible={this.props.visible}>
          Test
        </Modal>
      </div>
    );
  }
}

import React, { Component } from "react";
import { observer } from "mobx-react";
import Modal from 'react-modal';

import ChallengeModal from '../ChallengeModal/ChallengeModal';
import ModalHeader from './Modal/ModalHeader';
import ModalContent from './Modal/ModalContent';
import ModalFooter from './Modal/ModalFooter';

export default class JeopardyButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showModal: false
    };

    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
  }

  handleOpenModal() {
    this.setState({showModal: true});
  }

  handleCloseModal() {
    this.setState({showModal: false});
  }

  render () {
    const buttonStyle = {
      backgroundColor: (this.props.solved) ? 'green' : 'blue'
    };
    return (
      <div className='jeopardy-button'
        onClick={this.handleOpenModal}
        style={buttonStyle}>
        <a className='button'>{this.props.value}</a>
        <Modal 
           isOpen={this.state.showModal}
           contentLabel="onRequestClose Example"
           onRequestClose={this.handleCloseModal}
           className="modal"
           overlayClassName="modal-overlay"
           ariaHideApp={false}
        >
          <ModalHeader title={`${this.props.category} - ${this.props.name}`}
            handleClose={this.handleCloseModal}/>
          <ModalContent>
            <ChallengeModal />
          </ModalContent>
          <ModalFooter confirmText='Done'
            cancel={this.handleCloseModal}/>
        </Modal>
      </div>
    );
  }
};

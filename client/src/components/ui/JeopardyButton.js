import React, { Component } from "react";
import { observer } from "mobx-react";
import Modal from 'react-modal';
import axios from "axios";

import ChallengeModal from '../ChallengeModal';
import ModalHeader from './Modal/ModalHeader';
import ModalContent from './Modal/ModalContent';
import ModalFooter from './Modal/ModalFooter';

export default class JeopardyButton extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showModal: false
    };

    this.onSubmit = this.onSubmit.bind(this);
    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
  }

  handleOpenModal() {
    this.setState({showModal: true});
  }

  handleCloseModal() {
    this.setState({showModal: false});
  }

  popCorrectFlag(eleId) {
    var x = document.getElementById(eleId)
    x.className = "show";

    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 2000);
  }

  onSubmit(e, flag) {
    // flag check
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
    axios.defaults.withCredentials = true;
    const mutation = this.postFlag(flag);
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
      const status = response.data.data.checkFlag.status;

      if (status === "Correct Flag") {
        this.popCorrectFlag('correct-flag');
        this.handleCloseModal();
      } else if (status === "No currently active CTF") {
        this.popCorrectFlag('no-ctf');
      } else {
        this.popCorrectFlag('incorrect-flag');
      }
    })
  }

  postFlag(flag) {
    return `mutation { checkFlag ( flag: "${flag}") { status } }`;
  }

  render () {
    const buttonStyle = {
      display: (this.props.solved) ? 'none' : ''
    };
    const solvedStyle = {
      fill: (this.props.solved) ? '#de5917' : '#FFC07C'
    }

    // const buttonStyle = {
    //   backgroundColor: (this.props.solved) ? '#14af12' : '#2638ED'
    // };

    return (
      // TODO - Send hosted information to ChallengeModal

      <div className='question-block'
        onClick={this.handleOpenModal}>
        <svg width="76px" height="76px" viewBox="0 0 76 76"
          xmlns="http://www.w3.org/2000/svg">
        <path id="greyshadow" 
          d="M8 8h68v68h-68z"
          fill="#BFBFBF"/>
        <path id="blackborder" 
          d="M4 4h68v68h-68z"
          fill="#000"/>
        <path id="background" 
          d="M4 4h64v64h-64z"
          style={solvedStyle}/>
        <path id="borderlefttop" 
          d="M4 0h64M0 4v64" 
          stroke="#DE5917" 
          strokeWidth="8"/>
        <path id="rivets" 
          d="M8 8h4v4h-4zM60 60h4v4h-4zM8 60h4v4h-4zM60 8h4v4h-4z" 
          fill="#000"/>
        <path id="questionshadow" 
          style={buttonStyle}
          d="M24 20h4v-4h20v4h4v16h-8v8h-8v-8h4v-4h4v-12h-12v12h-8zM36 52h8v8h-8z" fill="#000"/>
        <path id="question" 
          style={buttonStyle}
          d="M20 16h4v-4h20v4h4v16h-8v8h-8v-8h4v-4h4v-12h-12v12h-8zM32 48h8v8h-8z" fill="#DE5917"/>
        </svg>
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
            <ChallengeModal sid={this.props.sid}
              name={this.props.name}
              solves={this.props.solves}
              value={this.props.value}
              description={this.props.description}
              path={this.props.path}
              fileUpload={this.props.fileUpload}
              hosted={this.props.hosted}
              downloadPath={this.props.downloadPath}
            />
          </ModalContent>
          <ModalFooter confirmText='Submit'
            confirm={this.onSubmit}/>
        </Modal>
        <div id="correct-flag">Correct Flag!</div>
        <div id="incorrect-flag">Incorrect Flag</div>
        <div id="no-ctf">No currently active CTF</div>
      </div>

      // <div className='jeopardy-button'
      //   onClick={this.handleOpenModal}
      //   style={buttonStyle}>
      //   <a className='button'>{this.props.value}</a>
      //   <Modal 
      //      isOpen={this.state.showModal}
      //      contentLabel="onRequestClose Example"
      //      onRequestClose={this.handleCloseModal}
      //      className="modal"
      //      overlayClassName="modal-overlay"
      //      ariaHideApp={false}
      //   >
      //     <ModalHeader title={`${this.props.category} - ${this.props.name}`}
      //       handleClose={this.handleCloseModal}/>
      //     <ModalContent>
      //       <ChallengeModal sid={this.props.sid}
      //         name={this.props.name}
      //         solves={this.props.solves}
      //         value={this.props.value}
      //         description={this.props.description}
      //         path={this.props.path}
      //         fileUpload={this.props.fileUpload}
      //         hosted={this.props.hosted}
      //         downloadPath={this.props.downloadPath}
      //       />
      //     </ModalContent>
      //     <ModalFooter confirmText='Submit'
      //       confirm={this.onSubmit}/>
      //   </Modal>

      //   <div id="correct-flag">Correct Flag!</div>
      //   <div id="incorrect-flag">Incorrect Flag</div>
      //   <div id="no-ctf">No currently active CTF</div>
      // </div>
    );
  }
};
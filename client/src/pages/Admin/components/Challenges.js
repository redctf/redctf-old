import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import axios from "axios";

import Modal from 'react-modal';
import ModalHeader from '../../../components/ui/Modal/ModalHeader';
import ModalContent from '../../../components/ui/Modal/ModalContent';
import ModalFooter from '../../../components/ui/Modal/ModalFooter';

import Icon from "../../../components/ui/SvgIcon/Icon";
import Button from '../../../components/ui/Button';

import AdminBox from './AdminBox';
import ChallengeStatus from './ChallengeStatus';
import CreateChallenge from './CreateChallenge';


@inject("store")
@observer
export default class Challenges extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
    this.state = {
      show: 'home',
      showModal: false,
      challenge: {
        title: '',
        category: 0,
        points: 0,
        description: '',
        flag: '',
        upload: null,
        imageName: '',
        hosted: false
      }
    };
  }

  addChallenge() {
    const c = this.state.challenge;
    return `mutation { addChallenge ( category: ${c.category}, description: "${c.description}", flag: "${c.flag}", points: ${c.points}, title: "${c.title}", hosted: ${c.hosted}, imageName: "${c.imageName}", ports: "${c.ports}", pathPrefix: "", upload: "${c.upload}" ) { status } }`
  }

  onSubmit = () => {
    // TODO - add in checks (i.e. do not allow submit if all fields not filled out properly)

    const port = 8000;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
    axios.defaults.withCredentials = true;

    const mutation = this.addChallenge();
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

  createNewChallenge = () => {
    this.setState({showModal: true});
  }

  handleCloseModal = () => {
    this.setState({showModal: false});
  }

  handleChallengeChanged = (challenge) => {
    this.setState(prevState => {
      return {
        challenge: challenge
      };
    });
  }

  render() {
    const challenges = this.store.appState.challenges.map((ele, idx) => {
      return (
        <ChallengeStatus key={idx} challenge={ele} />
      )
    });

    return (
      <div className='admin-section'>
        <div className='admin-sub-section'>
          <div className='admin-sub'>
            <Icon className='Icon'
              type='CUBES'
              viewBox='0 0 512 512'
            />
            <div className='admin-sub-title'>Existing Challenges</div>
          </div>
          <Button className='admin-sub'
            class='create-new-challenge-btn'
            title='Create New Challenge'
            icon='PLUS'
            viewBox='0 0 512 512'
            onClick={this.createNewChallenge}
          />
          <Modal 
             isOpen={this.state.showModal}
             contentLabel="created Modal"
             onRequestClose={this.handleCloseModal}
             className="modal"
             overlayClassName="modal-overlay"
             ariaHideApp={false}
          >
            <ModalHeader title='Create Challenge'
              handleClose={this.handleCloseModal}/>
            <ModalContent>
              <CreateChallenge onChange={this.handleChallengeChanged}/>
            </ModalContent>
            <ModalFooter confirmText='Submit'
              flagSubmissionInput={false}
              confirm={this.onSubmit}/>
          </Modal>
        </div>
        {challenges}
      </div>
    );
  }
}

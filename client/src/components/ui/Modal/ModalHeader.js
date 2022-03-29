import React, { Component } from "react";
import PropTypes from 'prop-types';

export default class ModalHeader extends Component {
  static displayName = 'ModalHeader';
  static propTypes = {
      title: PropTypes.string,
      closeButton: PropTypes.bool,
      handleClose: PropTypes.func
  };
  static defaultProps = {
      title: 'Modal',
      closeButton: true,
      handleClose() {}
  };
  constructor(props) {
      super(props);

      this.state = {
        number: 1,
        turts: [
          'leo',
          'raph',
          'donny',
          'mike'
        ]
      }

      this.handleClose = this.handleClose.bind(this);
  }

  generateRandomNumber = () => {
    console.log('generateRandomNumber', Math.floor(Math.random() * this.state.turts.length), this.state.number);
    return Math.floor(Math.random() * this.state.turts.length)
  }

  render() {
      const ninjaClass = this.state.turts[this.generateRandomNumber()];
      return (
           <div className='modal-header'>
              <div className='modal-title'>
                <div className={`ninja-turtle ${ninjaClass}`}>
                </div>
                {this.props.title}
              </div>
              {(this.props.closeButton) ? <div className='modal-close'
                  onClick={this.handleClose}></div> : null}
          </div>
      );
  }
  handleClose(evt) {
      this.props.handleClose(evt);
  }
};

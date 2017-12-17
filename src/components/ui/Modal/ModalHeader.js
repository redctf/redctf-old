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

      this.handleClose = this.handleClose.bind(this);
  }
  render() {
      return (
           <div className='modal-header'>
              <div className='modal-title'>{this.props.title}</div>
              {(this.props.closeButton) ? <div className='modal-close'
                  onClick={this.handleClose}></div> : null}
          </div>
      );
  }
  handleClose(evt) {
      this.props.handleClose(evt);
  }
};
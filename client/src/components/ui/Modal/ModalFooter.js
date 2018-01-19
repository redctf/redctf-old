import React, { Component } from "react";
import PropTypes from 'prop-types';
import Button from './ModalButton';

export default class ModalFooter extends Component {
  static displayName = 'ModalFooter';
  static propTypes = {
    confirmButton: PropTypes.bool,
    confirmDisabled: PropTypes.bool,
    cancelButton: PropTypes.bool,
    cancelDisabled: PropTypes.bool,
    flagSubmissionInput: PropTypes.bool,
    cancel: PropTypes.func,
    confirm: PropTypes.func,
    confirmText: PropTypes.string,
    confirmType: PropTypes.string,
    cancelText: PropTypes.string
  };
  static defaultProps = {
    cancelButton: false,
    confirmButton: true,
    cancelDisabled: false,
    confirmDisabled: false,
    flagSubmissionInput: true,
    cancel() {},
    confirm() {},
    confirmText: 'Confirm',
    confirmType: 'primary',
    cancelText: 'Cancel'
  };
  constructor(props) {
    super(props);

    this.handleConfirm = this.handleConfirm.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }
  render() {
    console.log('this.props.cancelText', this.props.cancelText);
    return (
      <div className='modal-footer'>
        {(this.props.cancelButton) ?
          <Button disabled={this.props.cancelDisabled}
            onClick={this.handleCancel}>{this.props.cancelText}</Button> : null}
        {(this.props.flagSubmissionInput) ?
          <input type="text"
            id="challengeFlag"
            className="temp-input"
            placeholder="flag"
            onChange={this.handleFieldChanged}/> : null }
        {(this.props.confirmButton) ?
          <Button onClick={this.handleConfirm}
            disabled={this.props.confirmDisabled}
            type={this.props.confirmType}>{this.props.confirmText}</Button> : null}
      </div>
    );
  }
  handleCancel(evt) {
    this.props.cancel(evt);
  }
  handleConfirm(evt) {
    this.props.confirm(evt);
  }
};

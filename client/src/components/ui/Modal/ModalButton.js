import React, { Component } from "react";
import PropTypes from 'prop-types';


const styles = {
  button: {
    padding: '9px 19px',
    borderRadius: '2px',
    borderStyle: 'solid',
    borderWidth: '1px',
    background: '#f4f4f4',
    fontWeight: 'bold',
    fontSize: '11px',
    cursor: 'pointer'
  },
};

export default class ModalButton extends Component {
  static displayName = 'ModalButton';
  static propTypes = {
    children: PropTypes.node,
    dataAuto: PropTypes.string,
    onClick: PropTypes.func,
    type: PropTypes.string,
    disabled: PropTypes.bool,
    class: PropTypes.string
  };
  static defaultProps = {
    dataAuto: 'button',
    onClick: function onClick() {},
    type: 'default',
    disabled: false
  };
  constructor(props) {
    super(props);

    this.handleClick = this.handleClick.bind(this);
  }
  render() {
    return (
      <button data-auto={this.props.dataAuto}
        type='button'
        onClick={!this.props.disabled && this.handleClick}
        className={`btn ${this.props.class}`}>{this.props.children}</button>
    );
  }
  handleClick(evt) {
    this.props.onClick(evt);
  }
};
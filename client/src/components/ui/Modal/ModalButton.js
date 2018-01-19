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
  default: {
    background: '#f4f4f4',
    borderColor: '#999999',
    ':hover': {
      borderColor: '#0285fc',
      color: '#0285fc'
    }
  },
  primary: {
    background: '#52a6fa',
    borderColor: '#0285fc',
    color: '#fff',
    ':hover': {
      background: '#0285fc',
      borderColor: '#0285fc'
    }
  },
  // need better names for green and red
  green: {
    background: '#8cc63f',
    borderColor: '#7db038',
    ':hover': {
      background: '#7eb239',
      borderColor: '#71a033'
    }
  },
  red: {
    background: '#e80a40',
    borderColor: '#ca0938',
    color: '#fff',
    ':hover': {
      color: '#fff',
      background: '#d00939',
      borderColor: '#bb0833'
    }
  },
  disabled: {
    opacity: '0.4',
    cursor: 'default',
    pointerEvents: 'none'
  }
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
    dataAuto: 'sgButton',
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
        onClick={!this.props.disabled && this.handleClick}
        className={this.props.class}>{this.props.children}</button>
    );
  }
  handleClick(evt) {
    this.props.onClick(evt);
  }
};
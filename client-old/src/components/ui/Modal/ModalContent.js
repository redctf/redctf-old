import React, { Component } from "react";
import PropTypes from 'prop-types';

export default class ModalContent extends Component {
  static displayName = 'ModalContent';
  static propTypes = {
    children: PropTypes.node,
    style: PropTypes.object,
    className: PropTypes.string
  };
  static defaultProps = {};
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className={`${this.props.className} model-content`}
        style={this.props.style}>
        {this.props.children}
      </div>
    );
  }
};

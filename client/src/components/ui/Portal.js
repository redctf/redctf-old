import React, { Component } from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

/* eslint-disable */
// This is a modified version of https://github.com/tajo/react-portal
export default class Portal extends Component {
  static displayName = 'Portal';
  static propTypes = {
    children: PropTypes.element.isRequired,
    className: PropTypes.string,
    closeOnEsc: PropTypes.bool,
    closeOnOutsideClick: PropTypes.bool,
    isOpened: PropTypes.bool,
    onClose: PropTypes.func,
    openByClickOn: PropTypes.element,
    style: PropTypes.object,
  }

  constructor() {
    super();
    this.state = {active: false};

    this.openPortal = this.openPortal.bind(this);
    this.closePortal = this.closePortal.bind(this);
    this.handleOutsideMouseClick = this.handleOutsideMouseClick.bind(this);
    this.handleKeydown = this.handleKeydown.bind(this);
    this.handleScroll = this.handleScroll.bind(this);
    this.portal = null;
    this.node = null;
    this.throttleTime = 0;
  }

  componentWillMount() {
    if (this.props.isOpened) {
      this.openPortal(this.props);
    }
  }

  componentDidMount() {
    if (this.props.closeOnEsc) {
      document.addEventListener('keydown', this.handleKeydown);
    }

    if (this.props.closeOnOutsideClick) {
      document.addEventListener('mousedown', this.handleOutsideMouseClick);
      document.addEventListener('touchstart', this.handleOutsideMouseClick);
    }

    if (this.props.closeOnOutsideScroll) {
      document.addEventListener('scroll', this.handleScroll, true);
    }
  }

  componentWillReceiveProps(newProps) {
    // portal's 'is open' state is handled through the prop isOpened
    if (typeof newProps.isOpened !== 'undefined') {
      if (newProps.isOpened) {
        if (this.state.active) {
          this.renderPortal(newProps);
        } else {
          this.openPortal(newProps);
        }
      }

      if (!newProps.isOpened && this.state.active) {
        this.closePortal();
      }
    }

    // portal handles its own 'is open' state
    if (typeof newProps.isOpened === 'undefined' && this.state.active) {
      this.renderPortal(newProps);
    }
  }

  componentWillUnmount() {
    if (this.props.closeOnEsc) {
      document.removeEventListener('keydown', this.handleKeydown);
    }

    if (this.props.closeOnOutsideClick) {
      document.removeEventListener('mousedown', this.handleOutsideMouseClick);
      document.removeEventListener('touchstart', this.handleOutsideMouseClick);
    }

    if (this.props.closeOnOutsideScroll) {
      document.removeEventListener('scroll', this.handleScroll, true);
    }
    this.closePortal();
  }

  render() {
    if (this.props.openByClickOn) {
      return (
        <div className='openByClickOn'
          onClick={this.openPortal.bind(this, this.props)}>{this.props.openByClickOn}</div>);
    } else {
      return null;
    }
  }

  renderPortal(props) {
    if (!this.node) {
      this.node = document.createElement('div');
      document.body.appendChild(this.node);
    }

    let children = props.children;
    // https://gist.github.com/jimfb/d99e0678e9da715ccf6454961ef04d1b
    if (typeof props.children.type === 'function') {
      children = cloneElement(props.children, { closePortal: this.closePortal });
    }

    this.portal = ReactDOM.unstable_renderSubtreeIntoContainer(
      this,
      children,
      this.node,
      this.props.onUpdate
    );
  }

  openPortal(props, e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }

    this.setState({active: true});
    this.renderPortal(props);
  }

  closePortal(node) {
    if (this.node) {
      ReactDOM.unmountComponentAtNode(this.node);
      document.body.removeChild(this.node);
    }
    this.portal = null;
    this.node = null;

    if (this.props.onClose) {
      this.props.onClose(node);
    }
  }

  handleOutsideMouseClick(e) {
    if (!this.state.active) { return; }
    if (isNodeInRoot(e.target, ReactDOM.findDOMNode(this.portal))) { return; }
    e.stopPropagation();
    this.closePortal(e.target);
  }

  handleKeydown(e) {
    // ESC
    if (e.keyCode === 27 && this.state.active) {
      this.closePortal();
    }
  }

  handleScroll(e) {
    if (Date.now() > this.throttleTime + 500) {
      this.throttleTime = Date.now();

      if (!this.state.active) { return; }
      if (isNodeInRoot(e.target, this.portal)) { return; }
      e.stopPropagation();
      this.closePortal(e.target);
    }
  }
}

export function isNodeInRoot(node, root) {
  while (node) {
    if (node === root) {
      return true;
    }
    node = node.parentNode;
  }
  return false;
}

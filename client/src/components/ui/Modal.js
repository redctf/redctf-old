import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Portal from './Portal';
import pureRender from 'pure-render-decorator';

const styles = {
  overlay: {
    background: 'rgba(0,0,0,0.5)',
    zIndex: 9999,
    width: '100%',
    height: '100%',
    position: 'fixed',
    visibility: 'hidden',
    opacity: '0',
    top: 0,
    left: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.3s'
  },
  modal: {
    fontFamily: '"Open Sans", sans-serif',
    background: '#fff',
    width: '500px',
    borderRadius: '3px',
    boxShadow: '0px 0px 8px 1px rgba(0,0,0,0.3)',
    transition: 'all 0.8s',
    marginTop: '-100vh'
  }
};

@pureRender
export default class Modal extends Component {
  static displayName = 'Modal';
  static propTypes = {
    children: PropTypes.node,
    visible: PropTypes.bool,
    handleClose: PropTypes.func,
    modalEnter: PropTypes.func,
    hideOnOuterClick: PropTypes.bool,
    width: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.number
    ]),
    maxHeight: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.number
    ]),
    style: PropTypes.oneOfType([
      PropTypes.object,
      PropTypes.array
    ]),
    className: PropTypes.string,
    modalStyle: PropTypes.oneOfType([
      PropTypes.object,
      PropTypes.array
    ]),
    dataAuto: PropTypes.string
  };
  static defaultProps = {
    visible: false,
    width: '500px',
    hideOnOuterClick: false,
    handleClose() {},
    modalEnter() {},
    dataAuto: 'modal'
  };
  constructor(props) {
    super(props);
    this.state = {
      transition: false,
      visibility: 'hidden',
      opacity: 0,
      active: false
    };
    this.modalEnter = this.modalEnter.bind(this);
    this.modalExit = this.modalExit.bind(this);
    this.handleOuterClick = this.handleOuterClick.bind(this);
    this.handleHide = this.handleHide.bind(this);
  }
  componentWillMount() {
    if (this.props.maxHeight) {
      styles.modal.maxHeight = this.props.maxHeight;
    }
  }
  componentWillReceiveProps(nextProps) {
    if (nextProps.visible === true && this.state.visibility !== 'visible') {
      this.modalEnter();
    } else if (nextProps.visible === false && this.state.visibility !== 'hidden') {
      this.modalExit();
    }
  }
  render() {
    this.modalWidth = this.props.width;

    if (!this.props.visible && !this.state.transition) {
      return null;
    }

    styles.overlay.visibility = this.state.visibility;
    styles.overlay.opacity = this.state.opacity;

    if (this.refs.modal && !this.state.transition) {
      styles.modal.marginTop = '0';
    }

    return (
      <Portal isOpened={this.state.active}>
        <div style={[styles.overlay, this.props.style]}
          onClick={this.handleOuterClick && this.props.hideOnOuterClick}
          data-modal='true'>
          <div data-auto={this.props.dataAuto}
            ref='modal'
            className={this.props.className || ''}
            style={[styles.modal, {width: this.modalWidth}, this.props.modalStyle]}>
            {this.props.children}
          </div>
        </div>
      </Portal>
    );
  }
  modalWidth = '500px';
  modalEnter() {
    this.setState({active: true},
      () => {
        setTimeout(() => {
          this.setState({
            visibility: 'visible',
            opacity: '1'
          }, () => {
            setTimeout(() => {
              const input = this.refs.modal.querySelector('textarea, input, button');
              if (input) {
                input.focus();
              }
              this.props.modalEnter();
            }, 800);
          });
        }, 10);});
  }
  modalExit() {
    styles.modal.marginTop = '-100vh';
    this.setState({
      visibility: 'hidden',
      opacity: '0',
      transition: true
    }, () => setTimeout(() => {
      this.setState({transition: false, active: false});
    }, 500));
  }
  handleOuterClick(evt) {
    if (evt.target.getAttribute('data-modal')) {
      this.handleHide();
    }
  }
  handleHide() {
    this.modalExit();
    this.props.handleClose();
  }
  reposition() {
    console.warn('You are calling modal.reposition which is deprecated, follow this stacktrace and remove whatever is calling this'); // eslint-disable-line no-console
  }
}

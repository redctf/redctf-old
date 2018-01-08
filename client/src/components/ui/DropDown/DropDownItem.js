import React, { Component } from "react";
import PropTypes from 'prop-types';

export default class DropDownItem extends Component {
  static displayName = 'DropDownItem';
  static propTypes = {
    children: PropTypes.node,
    onClick: PropTypes.func,
    placeHolder: PropTypes.bool,
    value: PropTypes.any,
    isSelected: PropTypes.bool,
    width: PropTypes.string,
    className: PropTypes.string,
    activeClassName: PropTypes.string
  };
  static defaultProps = {
    placeHolder: false,
    onClick: function onClick() {},
    className: ''
  };
  constructor(props) {
    super(props);
  }
  render() {
    let children = this.props.children;
    if (typeof children !== 'string' && this.props.isSelected) {
      children = React.Children.map(this.props.children, (child) => {
        const passProps = {};
        if (typeof child.type === 'function') {
          passProps.isSelected = true;
        }
        return React.cloneElement(child, {
          ...passProps
        });
      });
    }

    return (
      <div onClick={::this.handleClick}
        className={`drop-down__item
          ${this.props.className}
          ${(this.props.isSelected && 'drop-down__item--active') || ''}
          ${(this.props.isSelected && this.props.activeClassName) || ''}
          ${(this.props.placeHolder && 'drop-down__place-holder') || ''}`}
        style={{width: this.props.width}}>
        {children}
      </div>
    );
  }
  handleClick(evt) {
    if (!this.props.isSelected) {
      this.props.onClick(this.props.value, evt);
    }
  }
}

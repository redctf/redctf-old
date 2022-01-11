import React, { Component } from "react";
import PropTypes from 'prop-types';

export default class SelectedItem extends Component {
  static displayName = 'SelectedItem';
  static propTypes = {
    children: PropTypes.node,
    className: PropTypes.string
  };
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className={`drop-down__select-box--selected ${this.props.className || ''}`}>
        <i style={{fontSize: '9px'}}
          className='fa fa-check'/>
        <div className='drop-down__inline-element'>
          {React.cloneElement(this.props.children, {className: `drop-down__selected-item ${this.props.className}`})}
        </div>
      </div>
    );
  }
}

import React, { Component } from "react";
import PropTypes from 'prop-types';
import { inject, observer } from "mobx-react";

import Icon from "../../../components/ui/SvgIcon/Icon";

@inject("store")
@observer
export default class AdminBox extends Component {
  static displayName = 'AdminBox';
  static propTypes = {
    title: PropTypes.string,
    icon: PropTypes.string,
    viewBox: PropTypes.string
  }
  static defaultProps = {
    title: '',
    icon: '',
    viewBox: '0 0 24 24'
  }
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  render() {
    return (
      <div className='admin-box'>
        <Icon className="Icon" type={this.props.icon} viewBox={this.props.viewBox}/>
        <div className='box-text'>{this.props.title}</div>
      </div>
    );
  }
}
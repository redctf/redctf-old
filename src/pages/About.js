import React, { Component } from "react";
import { inject, observer } from "mobx-react";

@observer
export default class About extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {
    return (
      <div className="page posts">
        <h1>About Us</h1>
      </div>
    );
  }
}

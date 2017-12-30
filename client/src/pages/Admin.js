import React, { Component } from "react";
import { inject, observer } from "mobx-react";

@observer
export default class Admin extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {
    return (
      <div className="page posts">
        <h1>Admin Page</h1>
      </div>
    );
  }
}

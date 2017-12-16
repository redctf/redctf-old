import React, { Component } from "react";
import { inject, observer } from "mobx-react";

@observer
export default class Team extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {
    return (
      <div className="page posts">
        <h1>Team</h1>
      </div>
    );
  }
}

import React, { Component } from "react";

export default class TurtleSoup extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {
    return (
      <div className={`page posts`}>
        <div className='turtle-soup'>
        	<h4>{`kernel{53322d72086de5cb3a2dad77b385db2e}`}</h4>
        </div>
      </div>
    );
  }
}

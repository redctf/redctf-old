import React, { Component } from "react";
import axios from "axios";

export default class Admin extends Component {

  render() {
    return (
      <div className="page">
        <iframe className='admin-iframe'
          src={`${location.protocol}//${location.hostname}/adminpanel/`} /> 
      </div>
    );
  }
}

        
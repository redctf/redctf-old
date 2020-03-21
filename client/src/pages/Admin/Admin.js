import React, { Component } from "react";
import axios from "axios";

export default class Admin extends Component {
  // getAdminPanel = () => {
  //   const html = '<h1>Test</h1>';
  //   return {
  //     __html: html
  //   }
  // }

  render() {
    //const port = 8000;
    //src={`${location.protocol}//${location.hostname}:${port}/adminpanel/`} /> 
    return (
      <div className="page">
        <iframe className='admin-iframe'
          src={`${location.protocol}//${location.hostname}/adminpanel/`} /> 
      </div>
    );
  }
}

        
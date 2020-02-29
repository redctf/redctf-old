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
    // const adminPanel = this.getAdminPanel;
    // console.log('adminPanel', adminPanel);
    
    return (
      <div className="page posts">
        {/*<div dangerouslySetInnerHTML={this.adminPanel} />;*/}
        <iframe className='admin-iframe'
          src="http://localhost:8000/adminpanel/" /> 
      </div>
    );
  }
}

        
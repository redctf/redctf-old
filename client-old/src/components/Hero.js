import React, { Component } from "react";

export default class Hero extends Component {
  render() {
    return (
      <div>
        <header>
          <h1><span className="red">red</span>CTF</h1>
          <svg className="hero-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            <polygon fill="white" points="100 0 100 100 0 100"/>
          </svg>
        </header>
      </div>
    );
  }
}

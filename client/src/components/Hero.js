import React, { Component } from "react";

export default class Hero extends Component {
  render() {
    return (
      <div>
        <header>
          <h3 className='hero-font'>This time, it's all about <span className="red">family.</span></h3>
          <svg className="hero-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            <polygon fill="white" points="100 0 100 100 0 100"/>
          </svg>
        </header>
      </div>
    );
  }
}

import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Match, Link } from "react-router-dom";

import Protected from "../components/Protected";
import DataWrapper from "../components/DataWrapper";

import ChallengeRowCol from '../components/ChallengeRowCol';

@Protected
@DataWrapper
@observer
export default class Challenges extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {    
    const { 
      items,
      verticalChallengeOrientation
    } = this.store.appState;
    const categoryOrientationClass = verticalChallengeOrientation ? 'vertical' : 'horizontal';

    // Fake JSON Challenge Data - Ideally we'll query with just a teamId and return the following.
    const fakeCategoryData = [
      'Cryptography',
      'Forensics',
      'Miscellaneous',
      'Web',
      'Pwn'
    ];

    // Iterate over challenge category JSON 
    const categories = fakeCategoryData.map((category) => {
      return (
        <div key={category}
          className={`category-${categoryOrientationClass}`}>
          <ChallengeRowCol category={category}
            vertical={verticalChallengeOrientation}/>
        </div>
      )
    });

    return (
      <div className={`page posts post-${categoryOrientationClass}`}>
        {categories}
        <span className='legend'>
          <span className='solved-key'/> Solved
          <span className='unsolved-key'/> Unsolved
        </span>
      </div>
    );
  }
}

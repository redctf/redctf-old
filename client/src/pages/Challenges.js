import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Match, Link } from "react-router-dom";

import Protected from "../components/Protected";
import DataWrapper from "../components/DataWrapper";

import ChallengeRowCol from '../components/ChallengeRowCol';
//import axios from "axios";

@Protected
@DataWrapper
@inject("store")
@observer
export default class Challenges extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {    
    const { 
      categories,
      items,
      verticalChallengeOrientation,
      team
    } = this.store.appState;
    const categoryOrientationClass = verticalChallengeOrientation ? 'vertical' : 'horizontal';

    console.log('cats', categories);
    if (categories && categories[0].id == 'test') {
      categories.shift();
    }
    const categoryMap = categories.map((cat) => {
      return (
        <div key={cat.sid}
          className={`category-${categoryOrientationClass}`}>
          <ChallengeRowCol category={cat.name}
            categoryId={cat.sid}
            vertical={verticalChallengeOrientation}/>
        </div>
      )
    });

    return (
      <div>
        <div className={`page posts post-${categoryOrientationClass}`}>
          {categoryMap}
        </div>
{/*        <div className='legend'>
          <span className='solved-key'/> Solved
          <span className='unsolved-key'/> Unsolved
        </div>*/}
      </div>
    );
  }
}

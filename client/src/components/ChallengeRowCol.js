import React, { Component } from 'react';
import { inject, observer } from "mobx-react";

import JeopardyButton from './ui/JeopardyButton';

@inject("store")
@observer
export default class ChallengeRowCol extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  render() {
    const { challenges, categories } = this.store.appState;


    // Fake JSON Challenge Data - Ideally we'll query with just a teamId and Category and return the following.
    const fakeChallengeData = [
      {
        value: '100',
        name: 'challenge100',
        description: 'challenge100 Description',
        solved: true
      },
      {
        value: '200',
        name: 'challenge200',
        description: 'challenge200 Description',
        solved: true
      },
      {
        value: '300',
        name: 'challenge300',
        description: 'challenge300 Description',
        solved: false
      },
      {
        value: '400',
        name: 'challenge400',
        description: 'challenge400 Description',
        solved: true
      },
      {
        value: '500',
        name: 'challenge500',
        description: 'challenge500 Description',
        solved: false
      }
    ];

    // Default to horizontal challenge orientation unless 'vertical' is passed in as a prop
    const direction = this.props.vertical ? 'vertical' : 'horizontal';  

    const challengeData = challenges.map((challenge) => {
      if (challenge.category == this.props.categoryId) {
        return challenge;
      }
    });

    console.log('categories', categories);
    console.log('challenges', challenges);
    console.log('challengeData', challengeData);



    // Map over JSON challenge data

    const challengeRowCol = challengeData.map((challenge) => {
      return (
        <JeopardyButton key={`${challenge.id}`}
          value={challenge.points}
          name={challenge.title}
          category={this.props.category}
          description={challenge.description}
        />
      )
    });

    const category = (
      <span className='challengeCategory'>{this.props.category}</span>
    )

    return (
      <div className='challengeRowCol'>
        <div className={direction}>
          {category} {challengeRowCol}
        </div>
      </div>
    );
  }
}

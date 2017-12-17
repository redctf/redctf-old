import React, { Component } from 'react';

import JeopardyButton from '../ui/JeopardyButton';

export default class ChallengeRowCol extends Component {
  render() {
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

    // Map over JSON challenge data

    const challengeRowCol = fakeChallengeData.map((challenge) => {
      return (
        <JeopardyButton key={`${challenge.value}-${challenge.name}`}
          value={challenge.value}
          name={challenge.name}
          category={this.props.category}
          description={challenge.description}
          solved={challenge.solved}
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

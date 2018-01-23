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
    const {
      challenges,
      categories,
      team
    } = this.store.appState;

    // Default to horizontal challenge orientation unless 'vertical' is passed in as a prop
    const direction = this.props.vertical ? 'vertical' : 'horizontal';  

    const challengeData = challenges.filter((challenge) => {
      if (challenge.category == this.props.categoryId) {
        return challenge;
      }
    });

    // Get array of solved challenges
    const solved = this.store.appState.filterSingleTeam(team.id)[0].solved;

    // Map over JSON challenge data
    const challengeRowCol = challengeData.map((challenge) => {
      let challengeSolved = false;
      if (solved.includes(challenge.sid)) {
        challengeSolved = true;
      }
      return (
        <JeopardyButton key={`${challenge.id}`}
          value={challenge.points}
          name={challenge.title}
          category={this.props.category}
          description={challenge.description}
          solved={challengeSolved}
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

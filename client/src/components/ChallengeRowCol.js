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

    challengeData.sort(function(a,b){return (a.points > b.points) ? 1 : ((b.points > a.points) ? -1 : 0); } );

    // Get array of solved challenges
    const solved = this.store.appState.filterSingleTeam(team.id)[0].solved;

    // Map over JSON challenge data
    const challengeRowCol = challengeData.map((challenge) => {
      let challengeSolved = false;
      solved.forEach((solve) => {
        if (solve.id == challenge.sid) {
          challengeSolved = true;
        }
      });

      return (
        <JeopardyButton key={`${challenge.sid}`}
          value={challenge.points}
          name={challenge.title}
          category={this.props.category}
          description={challenge.description}
          solves={challenge.solved_count}
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

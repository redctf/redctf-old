import React, { Component } from "react";
import { inject, observer } from "mobx-react";

@inject("store")
@observer
export default class ChallengeStatus extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  getChallengeRows() {
    const categories = this.store.appState.categories;
    const challengeRows = this.store.appState.challenges.map((challenge) => {
      const categoryName = categories.filter((cat) => {
        if (cat.sid === challenge.category) {
          return cat;
        }
      });

      return (
        <div key={challenge.id}
          className='challenge-row'>
          <div className='challenge-row-problem'>
            <span className='challenge-row-span challenge-row-points'>
              <div className='challenge-row-heading'>POINTS</div>
              <div className='challenge-row-score'>{challenge.points}</div>
            </span>
            <span className='challenge-row-span'>
              <div className='challenge-row-heading'>CATEGORY</div>
              <div className='challenge-row-title'>{categoryName[0].name}</div>
            </span>
          </div>
          <div>
            <div className='challenge-row-heading'>TITLE</div>
            <div className='challenge-row-title'>{challenge.title}</div>
          </div>
          <div>
            <div className='challenge-row-heading'>SOLVES</div>
            <div className='challenge-row-score'>{challenge.solved_count}</div>
          </div>
          <div>
            <span><button type="button">Edit</button></span>
            <span><button type="button">Delete</button></span>
            <span><button type="button">Clone</button></span>
          </div>
        </div>
      );
    });

    return challengeRows;
  }

  render() {
    const challengeTable = this.getChallengeRows();
    return (
      <span>
        {challengeTable}
      </span>
    );
  }
}
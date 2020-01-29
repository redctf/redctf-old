import React, { Component } from "react";
import { inject, observer } from "mobx-react";

import Icon from "../../../components/ui/SvgIcon/Icon";

@inject("store")
@observer
export default class ChallengeStatus extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  render() {
    const challenge = this.props.challenge;
    const categoryName = this.store.appState.categories.filter((cat) => {
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
          <Icon className='challenge-status-icon'
            type='EDIT'
            viewBox='0 0 576 512'
          />
          <Icon className='challenge-status-icon'
            type='TRASH'
            viewBox='0 0 448 512'
          />
          <Icon className='challenge-status-icon'
            type='CLONE'
            viewBox='0 0 512 512'
          />
        </div>
      </div>
    );
  }
}

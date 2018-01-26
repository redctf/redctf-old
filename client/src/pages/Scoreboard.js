import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { XYFrame } from "semiotic";
@inject("store")
@observer
export default class Scoreboard extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  sortByPointsAndTimes(teams) {
    // primary sort is points
    // secondary sort is the earliest timestamp on the last challenge solve.
    const sortedTeams = teams.sort((a,b) => {
      return (+(b.points > a.points) || +(b.points === a.points) - 1) ||
        (+(a.solved[a.solved.length-1].timestamp > b.solved[b.solved.length-1].timestamp) || 
        +(a.solved[a.solved.length-1].timestamp === b.solved[b.solved.length-1].timestamp) - 1);
    });
    return sortedTeams;
  }

  getTeamRows(teams, challenges) {
    const totalChallenges = challenges.length;
    const teamRows = teams.map((team) => {
      return (
        <tr>
          <td className='temp-td'>{team.name}</td>
          <td className='temp-td'>{team.points}</td>
          <td className='temp-td'>{`${team.correct_flags}/${totalChallenges}`}</td>
          <td className='temp-td'>{team.timestamp}</td>
        </tr>
      );
    });
    return teamRows;
  }

  render() {
    const {
      challenges,
      teams
    } = this.store.appState;

    const teamRows = this.getTeamRows(this.sortByPointsAndTimes(teams), challenges);

    return (
      <div className="page posts">

        <div>Scoreboard</div>



        <table>
          <thead>
            <tr>
              <th className='temp-th'>Team Name</th>
              <th className='temp-th'>Score</th>
              <th className='temp-th'>Solved Challenges</th>
            </tr>
          </thead>
          <tbody>
            {teamRows}
          </tbody>
        </table>
      </div>
    );
  }
}

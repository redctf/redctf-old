import React, { Component } from "react";
import { inject, observer } from "mobx-react";

@inject("store")
@observer
export default class Scoreboard extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  sortByPoints(teams) {
    const sortedTeams = teams.sort((a,b) => {
      return (a.points > b.points) ? -1 : ((b.points > a.points) ? 1 : 0);
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

    const teamRows = this.getTeamRows(this.sortByPoints(teams), challenges);

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

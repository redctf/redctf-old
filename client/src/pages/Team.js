import React, { Component } from "react";
import PropTypes from 'prop-types';
import { inject, observer } from "mobx-react";
import { VictoryChart, VictoryGroup, VictoryTheme, VictoryLine, VictoryScatter, VictoryAxis, VictoryTooltip, VictoryLabel } from 'victory';

@inject('store')
@observer
export default class Team extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  getTeamRows(teams, challenges) {
    const totalChallenges = challenges.length;
    const teamRows = teams.map((team) => {
      return (
        <tr onClick={() => this.viewTeam(team.sid)}>
          <td>{team.name}</td>
          <td className='temp-td'>{team.points}</td>
          <td className='temp-td'>{`${team.correct_flags}/${totalChallenges}`}</td>
        </tr>
      );
    });
    return teamRows;
  }

  getGraphData() {
    // Only show top ten teams
    const teams = this.store.appState.teams.sort((a,b) => {
      return (a.points > b.points) ? -1 : ((b.points > a.points) ? 1 : 0);
    }).slice(0,10);
    const series = teams.map((team, i) => {
      let points = 0;
      const preferredColors = ['red', 'blue', 'green', 'orange', 'purple', 'deeppink', 'lightseagreen', 'navy', 'tomato', 'sienna'];  //TODO - more colors!
      const data = team.solved.map((challengeSolved) => {
        return {
          x: new Date(challengeSolved.timestamp * 1000),
          y: points += challengeSolved.points
        }
      });

      return (
        <VictoryGroup data={data}>
          <VictoryLine
            style={{
              data: { stroke: preferredColors[i] },
              parent: { border: "1px solid #ccc"}
            }}
          />
          <VictoryScatter
            style={{ data: { 
              fill: preferredColors[i],
              fillOpacity: ".7",
              stroke: preferredColors[i],
              strokeWidth: 1
            }}}
            labelComponent={<VictoryTooltip />}
            size={3}
          />
        </VictoryGroup>
      );
    });

    return series;
  }

  render() {
    const teamId = new URLSearchParams(location.search).get('id');
    const { challenges } = this.store.appState;

    const team = this.store.appState.filterSingleTeam(teamId)[0];
    //const teamRows = this.getTeamRows(teams, challenges);
    const series = this.getGraphData();

    console.log('team NOW', team);

    const challengeRows='';

    return (
      <div className='page posts'>
        <div className='graph-container'>
          <h2>{team.name}</h2>

          <VictoryChart
            animate={{
              duration: 2000,
              onLoad: { duration: 1000 }
            }}
            theme={VictoryTheme.material}
            width={600}
          >
            {series}
            <VictoryAxis fixLabelOverlap
              label="time (CST)"
              scale="time"
              style={{
                fontSize: 20,
                axisLabel: {padding: 36}
              }}
            />
            <VictoryAxis dependentAxis
              label="points"
              style={{
                fontSize: 20,
                axisLabel: {padding: 55}
              }}
            />
          </VictoryChart>

          <div className='table-container'>
            <table className='table table-bordered table-hover'>
              <thead>
                <tr>
                  <th className='temp-td'>Challenge Name</th>
                  <th className='temp-td'>Score</th>
                  <th className='temp-td'>Time Solved</th>
                </tr>
              </thead>
              <tbody>
                {challengeRows}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}
import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import { Link } from "react-router-dom";
import { VictoryChart, VictoryGroup, VictoryTheme, VictoryLine, VictoryScatter, VictoryAxis, VictoryTooltip, VictoryLabel } from 'victory';

@inject('store')
@observer
export default class Scoreboard extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }

  viewTeam(teamId) {
    this.props.history.push(`/team?id=${teamId}`);
  }

  getTeamRows(teams, challenges) {
    const totalChallenges = challenges.length;
    const teamRows = teams.map((team, idx) => {
      const preferredColors = ['red', 'blue', 'green', 'orange', 'purple', 'deeppink', 'lightseagreen', 'navy', 'tomato', 'sienna'];  //TODO - more colors!
      const rowStyle = preferredColors[idx];

      return (
        <tr onClick={() => this.viewTeam(team.sid)}
          key={team.sid}>
          <td>
            <span>{team.name}</span>
            <span style={{backgroundColor: rowStyle}}
              className='team-table-color'></span>
          </td>
          <td className='temp-td'>{team.points}</td>
          <td className='temp-td'>{`${team.correct_flags}/${totalChallenges}`}</td>
        </tr>
      );
    });
    return teamRows;
  }

  getGraphData() {
    const graphData = [{
      x: new Date(this.store.appState.ctfs[0].created * 1000),    // TODO horizon.ctf.start_time
      y: 0
    }];
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

      data.unshift(graphData[0]);

      return (
        <VictoryGroup data={data}
          key={`${team.name}-${i}`}>
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
    const {
      challenges,
      teams
    } = this.store.appState;

    const teamRows = this.getTeamRows(teams, challenges);
    const series = this.getGraphData();

    return (
      <div className='page posts'>
        <div className='graph-container'>
          <h2>Scoreboard</h2>

          <VictoryChart
            animate={{
              duration: 5000,
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
            <table className='table table-bordered table-hover scoreboard-table'>
              <thead>
                <tr>
                  <th className='temp-td'>Team Name</th>
                  <th className='temp-td'>Score</th>
                  <th className='temp-td'>Solved</th>
                </tr>
              </thead>
              <tbody>
                {teamRows}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}

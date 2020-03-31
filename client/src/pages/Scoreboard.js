import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import { Link } from "react-router-dom";
import { VictoryChart, VictoryGroup, VictoryTheme, VictoryLine, VictoryScatter, VictoryAxis, VictoryTooltip, VictoryLabel } from 'victory';

@inject('store')
@observer
export default class Scoreboard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      totalSolvedChallenges: 0
    };
    this.store = this.props.store;
  }

  componentDidMount() {
    const {teams} = this.store.appState;
    const teamsFiltered = teams.filter(t => !t.hidden);
    let total = 0;

    teamsFiltered.forEach((team) => {
      total += parseInt(team.correct_flags, 10);
      console.log('total', total);
    });
    
    console.log('total_post_loop', total);

    this.setState({
      totalSolvedChallenges: total
    });
    // console.log('totalChallenges: ', this.state.totalSolvedChallenges);
  }


  viewTeam(teamId) {
    this.props.history.push(`/teams?id=${teamId}`);
  }

  getTeamRows(teams, challenges) {
    const totalChallenges = challenges.length;
    const teamsFiltered = teams.filter(t => !t.hidden);
    const teamRows = teamsFiltered.map((team, idx) => {
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
      x: new Date(this.store.appState.ctfs[0].start * 1000),
      y: 0
    }];
    // Only show top ten teams with points
    const teamsFiltered = this.store.appState.teams.filter(t => !t.hidden).filter(r => r.points > 0).slice(0,10);
    const series = teamsFiltered.map((team, i) => {
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
                <tr>
                  <td>
                    <span>Total Challenges Solved</span>
                  </td>
                  <td className='temp-td'></td>
                  <td className='temp-td'>{this.state.totalSolvedChallenges}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }
}

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

  getTeamRows(data) {
    const categories = this.store.appState.categories;
    const teamRows = data.map((ele) => {
      const date = new Date(ele.timestamp * 1000);
      const categoryName = categories.map((cat) => {
        if (cat.sid === ele.category) {
          return cat.name;
        }
      });

      return (
        <tr key={ele.id}>
          <td>{categoryName}</td>
          <td className='temp-td'>{ele.points}</td>
          <td>{ele.title}</td>
          <td className='temp-td'>{`${date}`}</td>
        </tr>
      );
    });
    return teamRows;
  }

  getTeamData(team, challenges) {
    const data = [];
    team.solved.map((solve) => {
      challenges.forEach((challenge) => {
        if (challenge.sid === solve.id) {
          data.push({
            id: challenge.sid,
            category: challenge.category,
            title: challenge.title,
            points: solve.points,
            timestamp: solve.timestamp
          });
        }
      });
    });
    return data;
  }

  getGraphData(data) {
    const graphData = [{
      x: new Date(1517004800 * 1000),    // TODO horizon.ctf.start_time
      y: 0
    }];
    let points = 0;
    data.forEach((ele) => {
      points += ele.points;
      graphData.push({
        x: new Date(ele.timestamp * 1000),
        y: points
      })
    });
    return graphData;
  }

  render() {
    const teamId = new URLSearchParams(location.search).get('id');
    const { challenges } = this.store.appState;

    const team = this.store.appState.filterSingleTeam(teamId)[0];
    const data = this.getTeamData(team, challenges);
    const graphData = this.getGraphData(data);
    const challengeRows=this.getTeamRows(data);

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
            width={700}
          >
            <VictoryGroup data={graphData}>
              <VictoryLine
                style={{
                  data: { stroke: 'red' },
                  parent: { border: "1px solid #ccc"}
                }}
              />
              <VictoryScatter
                style={{ data: { 
                  fill: 'red',
                  fillOpacity: ".7",
                  stroke: 'red',
                  strokeWidth: 1
                }}}
                labelComponent={<VictoryTooltip />}
                size={3}
              />
            </VictoryGroup>
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
            <table className='table table-bordered table-hover team-table'>
              <thead>
                <tr>
                  <th>Category</th>
                  <th className='temp-td'>Score</th>
                  <th className='temp-td'>Challenge Name</th>
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
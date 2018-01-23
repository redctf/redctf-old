import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import axios from "axios";

@observer
export default class Team extends Component {
  constructor(props) {
    super(props);
    this.state = {
      teamId: null,
      teamName: '',
      teamPoints: 0
    };
    this.store = this.props.store;
  }

  getTeamInfo(e, flag) {
    // flag check
    const port = 8000;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
    axios.defaults.withCredentials = true;
    const query = this.queryTeam();
    axios.post('/graphql/',
      {
        query: query,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      }
    )
    .then((response) => {
      console.log('team information:', response);

      this.setState({
        teamId: response.data.data.team.id,
        teamName: response.data.data.team.name,
        teamPoints: response.data.data.team.points
      });
    })
  }

  queryTeam() {
    return `query { team {id name points users {id username}}}`;
  }

  componentWillMount() {
    // occurs directly before render method\
    this.getTeamInfo();
  }

  render() {
    return (
      <div className="page posts">
        <h1>Team: {this.state.teamName}</h1>
        <h3>TeamId: {this.state.teamId}</h3>
        <h3>Points: {this.state.teamPoints}</h3>
      </div>
    );
  }
}

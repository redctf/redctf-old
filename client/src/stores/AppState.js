import { observable, action, configure } from 'mobx';
import axios from 'axios';
configure({ enforceActions: "observed" });

async function getChallenges() {
  const mut = `query challenges {
    challenges {
      id
      title
      description
      category {
        id
      }
      points
      hosted
      fileUpload
      imageName
      ports
      pathPrefix
      upload
      created
    }
  }`;

  const jwt = sessionStorage.getItem('user') ? JSON.parse(sessionStorage.getItem('user')).token : '';

  axios.defaults.baseURL = `${window.location.protocol}//${window.location.hostname}`;
  axios.defaults.withCredentials = true;
  const res = await axios.post('/graphql/', {
    query: mut,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': `JWT ${jwt}`
    },
  });

  console.log('get challenges: ', res.data);
  return res.data;

  // const x = ['1','2','3','4','5','6','7','8','9','10'];
  // return x;
}


export class AppState {
  constructor() {
    this.token = '';
    this.team = {};
    // this.categories = [];
    this.challenges = [{completedTeams: ['1']}];
    this.teams = [];

    // footer value
    // TODO - move to a config file at some point
    this.footerValue = "Cobbled together by ";

    // if you want vertical orientation on your challenge board, set this to true.
    // TODO - move to a config file at some point
    this.verticalChallengeOrientation = true;

    //this.getCategories(); // initialize store observable categories
    this.getChallenges(); // initialize store observable challenges

  }

  // @computed teamsWithChallenges = () => {
  //   return this.teams.map((team) => {
  //     return {
  //       ...team,
  //       solved: this.challenges.filter((challenge) => {
  //         return team.solved.includes(challenge.id);
  //       }),
  //     };
  //   });
  // }
  
  @observable challenges = [];

  @action setToken = (login) => {
    console.log('setToken: ', login.token);
    this.token = login.token;
  }

  @action getChallenges = () => {
    this.challenges = getChallenges();
    return this.challenges;
  }

  // @action setChallengeComplete(team, chalenge) = () {
  //   this.team[team].solved.push(chalenge);
  // }
}

export default new AppState();
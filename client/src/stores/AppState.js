import { observable, action } from "mobx";
import axios from "axios";

export default class AppState {
  @observable authenticated;
  @observable authenticating;
  @observable items;
  @observable item;
  @observable team;
  @observable teams;
  @observable categories;
  @observable challenges;
  @observable testval;

  constructor() {
    this.authenticated = false;
    this.team = {};
    this.items = [];
    this.item = {};
    this.isSuperuser = false;
    this.categories = [];
    this.challenges = [];
    this.teams = [];

    // footer value
    this.testval = "Cobbled together by ";

    // if you want vertical orientation on your challenge board, set this to true.
    this.verticalChallengeOrientation = false;
  }

  // async fetchData(pathname, id) {
  //   let { data } = await axios.get(
  //     `https://jsonplaceholder.typicode.com${pathname}`
  //   );
  //   console.log(data);
  //   data.length > 0 ? this.setData(data) : this.setSingle(data);
  // }

  @action setData(data) {
    this.items = data;
  }

  @action setSingle(data) {
    this.item = data;
  }

  @action clearItems() {
    this.items = [];
    this.item = {};
  }

  @action filterSingleTeam(id) {
    return this.teams.filter((team) => {
      return (team.sid == id);
    });
  }

  @action authenticate() {
    return new Promise((resolve, reject) => {
      this.authenticating = true;
      setTimeout(() => {
        this.authenticated = !this.authenticated;
        this.authenticating = false;
        resolve(this.authenticated);
      }, 0);
    });
  }
}

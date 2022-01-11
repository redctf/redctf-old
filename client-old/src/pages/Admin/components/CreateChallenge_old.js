import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Tab, Tabs, TabPanel, TabList } from 'react-web-tabs';
import axios from "axios";

import DropDown from '../../../components/ui/DropDown/DropDown';
import DropDownItem from '../../../components/ui/DropDown/DropDownItem';
import SelectedItem from '../../../components/ui/DropDown/SelectedItem';
import ChallengeStatus from 'ChallengeStatus';
import Icon from "../../../components/ui/SvgIcon/Icon";

@inject("store")
@observer
export default class CreateChallenge extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
    this.state = {
      challenge: {
        title: '',
        category: 0,
        points: 0,
        description: '',
        flag: ''
      },
      category: ''
    };
    this.getCategories = ::this.getCategories;
  }

  addChallenge() {   
    // TODO - this is goofy logic, but works
    const categories = this.store.appState.categories;
    categories.sort(function(a,b){return (a.sid > b.sid) ? 1 : ((b.sid > a.sid) ? -1 : 0); } );
    const c = this.state.challenge;
    const category = categories[c.category].sid;
    
    console.log('4');
    return `mutation { addChallenge(flag: "${c.flag}" category: ${category} title: "${c.title}" points: ${c.points} description: "${c.description}") { status } }`;
  }

  addCategory() {
    console.log('7');
    return `mutation { addCategory(name: "${this.state.category}") { status } }`;
  }

  onSubmit(e) {
    console.log('6');
    if (this.state.challenge.category) {
      axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
      axios.defaults.withCredentials = true;

      const mutation = this.addChallenge();
      axios.post('/graphql/',
        {
          query: mutation,
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
          },
        }
      )
      .then((response) => {
        console.log(response);
      })
    }
  }
  
  onCategorySubmitted(e) {
    console.log('5');
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
    const mutation = this.addCategory();
    axios.post('/graphql/',
      {
        query: mutation,
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
      }
    )
    .then((response) => {
      console.log(response);
    })
  }

  handleFieldChanged = (e) => {
    const challenge = {...this.state.challenge};
    challenge[e.currentTarget.id] = e.currentTarget.value;
    this.setState({challenge});
    console.log('3');
  }

  handleCategoryChanged = (e) => {
    this.setState({category: e.currentTarget.value});
    console.log('2');
  }

  handleSelection = (selectedIndex, value, e) => {
    const challenge = {...this.state.challenge};
    challenge.category = value
    this.setState({challenge});
    console.log('1');
  }

  getCategories() {
    const categories = this.store.appState.categories;
    let items = null;

    if (categories.length == 0 || categories[0].id !== 'test') {
      categories.unshift({
        id: 'test',
        name: 'Please select a category',
        sid: 0
      });
    }

    if (categories.length !== 0) {
      categories.sort(function(a,b){return (a.sid > b.sid) ? 1 : ((b.sid > a.sid) ? -1 : 0); } );

      items = categories.map((ele, idx) => {
        return (
          <DropDownItem onClick={this.handleSelection.bind(this, ele)}
            key={ele.sid}
            value={idx}>
            <span>{ele.name}</span>
          </DropDownItem>
        );
      });
    }
    return items;  
  }

  validateInput = (event, maxLength, regex) => {
    const charCode = event.which;
    if (charCode === 0) {
      return;
    }

    const charStr = String.fromCharCode(charCode);

    if ((!regex.test(charStr) || event.target.value.length >= maxLength) && (event.which !== 8)) {
      event.preventDefault();
    }
  }

  render() {
    const categories = this.getCategories();
    categories.sort(function(a,b){return (a.sid > b.sid) ? 1 : ((b.sid > a.sid) ? -1 : 0); } );
    return (
      <div className="page posts">
        <div className="temp-section">
          <div className="temp-header">Create Challenge</div>
          <div className="temp-form">
            <ul className="temp-flex">
              <li>
                <label>Category</label>
                <DropDown width={460}
                    selectedItem={this.state.challenge.category}
                    selectedListItem={<SelectedItem/>}>
                    {categories}
                </DropDown>
                <span className='requiredStar'>*</span>
              </li>
              <li>
                <label>Title</label>
                <input type="text"
                  id="title"
                  className="temp-input"
                  placeholder="Awesome Laser Challenge"
                  onChange={this.handleFieldChanged}/>
                <span className='requiredStar'>*</span>
              </li>
              <li>
                <label>Points</label>
                <input type="text"
                  id="points"
                  className="temp-input"
                  placeholder="It's over 9000"
                  onKeyPress={(event) => {this.validateInput(event, 10, /^\d+$/);}}
                  onChange={this.handleFieldChanged}/>
                <span className='requiredStar'>*</span>
              </li>
              <li>
                <label>Description</label>
                <textarea rows="6"
                  id="description"
                  className="temp-input"
                  placeholder="Duck the lasers, steal the egg. Simple."
                  onChange={this.handleFieldChanged}>
                </textarea>
                <span className='requiredStar'>*</span>
              </li>
              <li>
                <label>Flag</label>
                <input type="text"
                  id="flag"
                  className="temp-input"
                  placeholder="ctf{flagformat}"
                  onChange={this.handleFieldChanged}/>
                <span className='requiredStar'>*</span>
              </li>
              <li><small className='requiredText'>* required</small></li>
              <li>
                <button type="button"
                  onClick={this.onSubmit.bind(this)}>Submit</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }
}
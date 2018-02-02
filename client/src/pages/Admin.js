import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import DropDown from '../components/ui/DropDown/DropDown';
import DropDownItem from '../components/ui/DropDown/DropDownItem';
import SelectedItem from '../components/ui/DropDown/SelectedItem';
import axios from "axios";

@inject("store")
@observer
export default class Admin extends Component {
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
    return `mutation { addChallenge(flag: "${c.flag}" category: ${category} title: "${c.title}" points: ${c.points} description: "${c.description}") { status } }`;
  }

  addCategory() {
    return `mutation { addCategory(name: "${this.state.category}") { status } }`;
  }

  onSubmit(e) {
    if (this.state.challenge.category) {
      const port = 8000;
      axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
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
    const port = 8000;
    axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
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
  }

  handleCategoryChanged = (e) => {
    this.setState({category: e.currentTarget.value});
  }

  handleSelection = (selectedIndex, value) => {
    const challenge = {...this.state.challenge};
    challenge.category = value
    this.setState({challenge});
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
        <div className="page-header">Admin Panel</div>

        {/* temporary section for creating categories */}
        <div className="temp-section">
          <div className="temp-header">Create Category</div>
          <div className="temp-form">
            <ul className="temp-flex">
              <li>
                <label>Category</label>
                <input type="text"
                  id="title"
                  className="temp-input"
                  placeholder="Cool Category"
                  onChange={this.handleCategoryChanged}/>
                <span className='requiredStar'>*</span>
              </li>
              <li><small className='requiredText'>* required</small></li>
              <li>
                <button type="button"
                  onClick={this.onCategorySubmitted.bind(this)}>Submit</button>
              </li>
            </ul>
          </div>
        </div>

        {/* temporary section for creating challenge */}
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

        {/* this section will contain hint releases */}
        <div className="temp-section">
          <div className="temp-header">Challenge Status</div>
          <div>

          </div>
        </div>


      </div>
    );
  }
}

import React, { Component } from "react";
import { inject, observer } from "mobx-react";
// import { Tab, Tabs, TabPanel, TabList } from 'react-web-tabs';
import axios from "axios";

// import DropDown from '../../components/ui/DropDown/DropDown';
// import DropDownItem from '../../components/ui/DropDown/DropDownItem';
// import SelectedItem from '../../components/ui/DropDown/SelectedItem';
// // import ChallengeStatus from './components/ChallengeStatus';
// // import CreateChallenge from './components/CreateChallenge';
import Icon from "../../components/ui/SvgIcon/Icon";




import AdminBox from './components/AdminBox';
import Challenges from './components/Challenges';



@inject("store")
@observer
export default class Admin extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
    this.state = {
      show: 'home',
      showBackBtn: false,
      showBackState: '',
      challenge: {
        title: '',
        category: 0,
        points: 0,
        description: '',
        flag: ''
      },
      category: ''
    };
  }

  onUseFeature(ele) {
    this.setState({
      show: ele
    });
  }

  handleBackBtn() {
    const newShow = this.state.showBackState;

    this.setState({
      show: newShow,
      showBackBtn: false,
      showBackState: ''
    });

    console.log(this.state);
  }

  // addChallenge() {   
  //   // TODO - this is goofy logic, but works
  //   const categories = this.store.appState.categories;
  //   categories.sort(function(a,b){return (a.sid > b.sid) ? 1 : ((b.sid > a.sid) ? -1 : 0); } );
  //   const c = this.state.challenge;
  //   const category = categories[c.category].sid;
    
  //   console.log('4');
  //   return `mutation { addChallenge(flag: "${c.flag}" category: ${category} title: "${c.title}" points: ${c.points} description: "${c.description}") { status } }`;
  // }

  // addCategory() {
  //   console.log('7');
  //   return `mutation { addCategory(name: "${this.state.category}") { status } }`;
  // }

  // onSubmit(e) {
  //   console.log('6');
  //   if (this.state.challenge.category) {
  //     const port = 8000;
  //     axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
  //     axios.defaults.withCredentials = true;

  //     const mutation = this.addChallenge();
  //     axios.post('/graphql/',
  //       {
  //         query: mutation,
  //         headers: {
  //           'Accept': 'application/json',
  //           'Content-Type': 'application/json',
  //         },
  //       }
  //     )
  //     .then((response) => {
  //       console.log(response);
  //     })
  //   }
  // }
  
  // onCategorySubmitted(e) {
  //   console.log('5');
  //   const port = 8000;
  //   axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
  //   const mutation = this.addCategory();
  //   axios.post('/graphql/',
  //     {
  //       query: mutation,
  //       headers: {
  //         'Accept': 'application/json',
  //         'Content-Type': 'application/json',
  //       },
  //     }
  //   )
  //   .then((response) => {
  //     console.log(response);
  //   })
  // }

  // handleFieldChanged = (e) => {
  //   const challenge = {...this.state.challenge};
  //   challenge[e.currentTarget.id] = e.currentTarget.value;
  //   this.setState({challenge});
  //   console.log('3');
  // }

  // handleCategoryChanged = (e) => {
  //   this.setState({category: e.currentTarget.value});
  //   console.log('2');
  // }

  // handleSelection = (selectedIndex, value, e) => {
  //   const challenge = {...this.state.challenge};
  //   challenge.category = value
  //   this.setState({challenge});
  //   console.log('1');
  // }

  // getCategories() {
  //   const categories = this.store.appState.categories;
  //   let items = null;

  //   if (categories.length == 0 || categories[0].id !== 'test') {
  //     categories.unshift({
  //       id: 'test',
  //       name: 'Please select a category',
  //       sid: 0
  //     });
  //   }

  //   if (categories.length !== 0) {
  //     categories.sort(function(a,b){return (a.sid > b.sid) ? 1 : ((b.sid > a.sid) ? -1 : 0); } );

  //     items = categories.map((ele, idx) => {
  //       return (
  //         <DropDownItem onClick={this.handleSelection.bind(this, ele)}
  //           key={ele.sid}
  //           value={idx}>
  //           <span>{ele.name}</span>
  //         </DropDownItem>
  //       );
  //     });
  //   }
  //   return items;  
  // }

  // validateInput = (event, maxLength, regex) => {
  //   const charCode = event.which;
  //   if (charCode === 0) {
  //     return;
  //   }

  //   const charStr = String.fromCharCode(charCode);

  //   if ((!regex.test(charStr) || event.target.value.length >= maxLength) && (event.which !== 8)) {
  //     event.preventDefault();
  //   }
  // }

  callbackFunction = (childShowBackBtn, childBackState) => {
    this.setState({
      showBackBtn: childShowBackBtn,
      showBackState: childBackState
    });
  }

  render() {
    return (
      <div className="page posts">
        <div className='admin-section'>

          <div className='admin-title-row'>
            <div className='admin-title'>Admin Panel</div>
            <div className='icon-area'>
              {this.state.showBackBtn && <div className='admin-back-icon'
                onClick={() => this.handleBackBtn()}>
                <Icon className="Icon"
                  viewBox='0 0 512 512'
                  type="BACK" />
              </div>}
              <div className='admin-home-icon'
                onClick={() => this.onUseFeature('home')}>
                <Icon className="Icon"
                  viewBox='0 0 576 512'
                  type="HOME" />
              </div>
            </div>
          </div>

          {this.state.show === 'home' && 
            <div className='admin-box-section'>
              <div onClick={() => this.onUseFeature('dashboard')}>
                <AdminBox title='Dashboard' 
                  icon='THLIST'
                  viewBox='0 0 512 512'/>
              </div>

              <div onClick={() => this.onUseFeature('challenges')}>
                <AdminBox title='Challenges' 
                  icon='CUBES'
                  viewBox='0 0 512 512'/>
              </div>

              <div onClick={() => this.onUseFeature('categories')}>
                <AdminBox title='Categories' 
                  icon='TABLE'
                  viewBox='0 0 512 512'/>
              </div>

              <div onClick={() => this.onUseFeature('settings')}>
                <AdminBox title='Settings'
                  icon='TOOLS'
                  viewBox='0 0 512 512'/>
              </div>

              <div onClick={() => this.onUseFeature('containers')}>
                <AdminBox title='Containers'
                  icon='DOCKER'
                  viewBox='0 0 640 512'/>
              </div>
            </div>
          }

          {this.state.show === 'dashboard' && 
            <div className='dashboard'>
              Dashboard
            </div>
          }

          {this.state.show === 'challenges' && 
            <div className='challenges'>
              <Challenges parentCallback={this.callbackFunction}/>
            </div>
          }

          {this.state.show === 'categories' && 
            <div className='categories'>
              Categories
            </div>
          }

          {this.state.show === 'settings' && 
            <div className='settings'>
              Settings
            </div>
          }

          {this.state.show === 'containers' && 
            <div className='containers'>
              Containers
            </div>
          }


        </div>
      </div>
    );
  }
}


{/*

        <Tabs defaultTab="vertical-tab-one" vertical>
          <TabList>
            <Tab tabFor="vertical-tab-one">
              <Icon className="Icon" type="CHALLENGES" />
            </Tab>
            <Tab tabFor="vertical-tab-two">Create Category</Tab>
            <Tab tabFor="vertical-tab-three">Create Challenge</Tab>
          </TabList>
          <TabPanel tabId="vertical-tab-one">
            <ChallengeStatus />
          </TabPanel>
          <TabPanel tabId="vertical-tab-two">
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
          </TabPanel>
          <TabPanel tabId="vertical-tab-three">
            <CreateChallenge />
          </TabPanel>
        </Tabs>*/}
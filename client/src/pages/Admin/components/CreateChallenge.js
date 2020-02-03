import React, { Component } from "react";
import { inject, observer } from "mobx-react";

import DropDown from '../../../components/ui/DropDown/DropDown';
import DropDownItem from '../../../components/ui/DropDown/DropDownItem';
import SelectedItem from '../../../components/ui/DropDown/SelectedItem';

import Icon from "../../../components/ui/SvgIcon/Icon";
import Button from '../../../components/ui/Button';

@inject("store")
@observer
export default class CreateChallenge extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
    this.state = {
      challenge: {
        title: '',
        categorySelected: 0,
        category: 0,
        points: 0,
        description: '',
        flag: '',
        upload: null,
        imageName: '',
      	hosted: false,
      	ports: ''
      },
      categories: null,
      hostedType: 'dockerfile'
    };
  }

  componentWillMount() {
  	const categories = this.store.appState.categories.sort(function(a,b){return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0); } );
    const challenge = {...this.state.challenge};
    challenge['category'] = categories[0].sid;
  	this.setState({challenge});
  }

  handleFieldChanged = (e) => {
    const challenge = {...this.state.challenge};
    challenge[e.currentTarget.id] = e.currentTarget.value;
    this.setState({challenge});
    this.props.onChange(challenge);
  }

  handleHostedChanged = (e) => {
  	const challenge = {...this.state.challenge};
  	challenge['hosted'] = !(this.state.challenge.hosted)
  	this.setState({challenge});
    this.props.onChange(challenge);
  }

  handleHostedChoice = (e) => {
    console.log(e);
  	this.setState({
  		hostedType: e.currentTarget.value
  	});
  }

  handleUpload = (e) => {
  	const challenge = {...this.state.challenge};
  	challenge['upload'] = e.target.files[0];
  	this.setState({challenge});
    this.props.onChange(challenge);
  }

  handleSelection = (selectedIndex, value, e) => {
    const challenge = {...this.state.challenge};
    challenge['category'] = selectedIndex.sid;
    challenge['categorySelected'] = value;
    this.setState({challenge});
    this.props.onChange(challenge);
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
    const categories = this.store.appState.categories.sort(function(a,b){return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0); } );
    const dropDownItems = categories.map((ele, idx) => {
      return (
        <DropDownItem onClick={this.handleSelection.bind(this, ele)}
          key={ele.sid}
          value={idx}>
          <span>{ele.name}</span>
        </DropDownItem>
      );
    });

    return (
      <div className="create-challenge-modal">

      	<DropDown selectBoxClassName='form-control category-selection'
      		menuClassName='category-selection-menu'
      		width={452}
      		selectedItem={this.state.challenge.categorySelected}
      		selectedListItem={<SelectedItem/>}>
      		{dropDownItems}
      	</DropDown>


      	<input type="text"
          id="title"
          className="form-control"
          placeholder="Title"
          onChange={this.handleFieldChanged}
         />

      	<textarea type="text"
      		rows="3"
          id="description"
          className="form-control"
          placeholder="Challenge Description"
          onChange={this.handleFieldChanged}
         />

        <div className='challenge-modal-double-line'>
        	<div className='challenge-modal-flag'>
		      	<input type="text"
		          id="flag"
		          className="form-control"
		          placeholder="Flag"
		          onChange={this.handleFieldChanged}
		         />
	        </div>
	        <div className='challenge-modal-points'>
		      	<input type="text"
		          id="points"
		          className="form-control"
		          placeholder="Points"
		          onKeyPress={(event) => {this.validateInput(event, 10, /^\d+$/);}}
		          onChange={this.handleFieldChanged}
		         />
	         </div>
         </div>


        <div className='hosted-radio-section'>
        	{/* TODO - Change to Hosted, add Tool Tips */}
        	<div className='hosted-radio-title'>Is Challenge Containerized?</div>
        	<div className='hosted-radios'>
						<div className='hosted-radio-button'
              onClick={this.handleHostedChanged}>
							<input type="radio"
								name="hosted-containers"
			 					checked={this.state.challenge.hosted}
								value={true}/>
							<label className='radio-label'
                htmlFor="Yes"> Yes</label>
						</div>
						<div className='hosted-radio-button'
                onClick={this.handleHostedChanged}>
			 				<input type="radio"
			 					name="hosted-containers"
			 					checked={!this.state.challenge.hosted}
			 					value={false}/>
			 				<label className='radio-label'
                htmlFor="No"> No</label>
		 				</div>
	 				</div>
 				</div>


        {this.state.challenge.hosted && 
        <div className='hosted-radio-section'>
        	<div className='hosted-radio-title'>How would you like to load container?</div>
        	<div className='hosted-radios'>
						<div className='hosted-radio-button'
                onClick={this.handleHostedChoice}>
							<input type="radio"
								name="hosted-type"
			 					checked={this.state.hostedType === 'dockerfile'}
								value={'dockerfile'}/>
							<label className='radio-label'
                htmlFor="dockerfile"> Use Dockerfile</label>
						</div>
						<div className='hosted-radio-button'
                onClick={this.handleHostedChoice}>
			 				<input type="radio"
			 					name="hosted-type"
			 					checked={this.state.hostedType === 'dockerhub'}
			 					value={'dockerhub'}/>
			 				<label className='radio-label'
                htmlFor="dockerhub"> Use Docker Hub</label>
		 				</div>
	 				</div>
 				</div>}


 				{this.state.challenge.hosted && this.state.hostedType === 'dockerfile' &&
 				<div className='hosted-type-section'>
 					<div className='hosted-type-desc'><b>Task: </b> Load a local Dockerfile.</div>
 					<div className='hosted-type-input'>
		      	<input type="file"
		          id="upload"
		          className="form-control"
		          placeholder="Upload local Dockerfile"
		          onChange={this.handleUpload}
		         />
 					</div>
 				</div>}

 				{this.state.challenge.hosted && this.state.hostedType === 'dockerhub' &&
 				<div className='hosted-type-section'>
 					<div className='hosted-type-desc'><b>Task: </b> Input the image name from Docker Hub and the ports that you would like it hosted on in a comma-separated list.</div>
 					<div className='challenge-modal-double-line'>
 						<div className='challenge-modal-image-name'>
			      	<input type="text"
			          id="imageName"
			          className="form-control"
			          placeholder="Image Name from Docker Hub"
			          onChange={this.handleFieldChanged}
			         />
		         </div>
 						<div className='challenge-modal-ports'>
			      	<input type="text"
			          id="ports"
			          className="form-control"
			          placeholder="Ports (comma-sep)"
			          onChange={this.handleFieldChanged}
			         />
		         </div>
 					</div>
 				</div>}
      </div>
    );
  }
}
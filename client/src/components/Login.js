import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Redirect } from "react-router-dom";
import axios from "axios";

@inject("store")
@observer
export default class Login extends Component {
	constructor(props) {
		super(props);
	}

	onSubmit(event) {
		const port = 8000;
		axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
		const mutation = this.postLogin("ryan", "abcd1234");
		axios.post('/graphql/',
			{
				query: mutation,
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
				},
			}
	  )
	  .then(function (response) {
	    console.log(response);
	  })
	  .catch(function (error) {
	    console.log(error);
	  });
	}

	postLogin(username, password) {
		return `mutation { login ( username: "${username}", password: "${password}") {status} }`;
	}


	whoami() {
		const port = 8000;
		axios.defaults.baseURL = `${location.protocol}//${location.hostname}:${port}`;
		axios.post('/graphql/',
			{
				query: "query{me}",
				headers: {
					'Accept': 'application/json',
					'Content-Type': 'application/json',
				},
			}
	  )
	  .then(function (response) {
	    console.log(response);
	  })
	  .catch(function (error) {
	    console.log(error);
	  });
	}

	render() {
		return (
			<div className="page login">
				
				<form>
					<input type="text" placeholder="name"/>
					<input type="text" placeholder="password"/>
				</form>
				<button type="button" onClick={this.onSubmit.bind(this)}>Login</button>


				<button type="button" onClick={this.whoami.bind(this)}>whoami</button>




				{this.props.store.authenticated &&
					!this.props.store.authenticating &&
					<Redirect to="/" />}
			</div>
		);
	}
}

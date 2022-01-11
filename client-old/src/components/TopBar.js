import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Link, withRouter } from "react-router-dom";
import axios from "axios";

import TopNav from "./TopNav";
import ActiveLink from "./ui/ActiveLink";
import Button from "./ui/Button";

@withRouter
@inject("store")
@observer
export default class TopBar extends Component {
	constructor(props) {
		super(props);
		this.store = this.props.store.appState;
	}

	authenticate(e) {
		if (e) e.preventDefault();
		
		// log out of back end
		if (this.store.authenticated) {
			axios.defaults.baseURL = `${location.protocol}//${location.hostname}`;
			axios.defaults.withCredentials = true;
			const mutation = this.postLogout();
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

		// change authenticated in AppState
		this.store.authenticate();
	}

	postLogout() {
		return `mutation { logout {status} }`;
	}

	render() {
		const { authenticated, isSuperuser } = this.store;
		const teamName = this.store.team ? this.store.team.name : '';
		const teamIdParam = this.store.team ? `id=${this.store.team.id}` : '';

		return (
			<div className="topbar">
				{authenticated && <TopNav location={this.props.location} />}
				{authenticated && <span className='team-name'><ActiveLink to="/teams" teamId={teamIdParam}>{teamName}</ActiveLink></span>}
				{authenticated && isSuperuser && <span className='team-name'><ActiveLink to="/admin">Admin</ActiveLink></span>}
				{authenticated && <Button
					onClick={this.authenticate.bind(this)}
					title={authenticated ? "Log out" : "Sign in"}
				/>}
			</div>
		);
	}
}

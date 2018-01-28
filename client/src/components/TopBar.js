import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Link, withRouter } from "react-router-dom";

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
		this.store.authenticate();
	}

	render() {
		const { authenticated, isSuperuser } = this.store;
		const teamName = this.store.team ? this.store.team.name : '';
		const teamIdParam = `id=${this.store.team.id}`;

		return (
			<div className="topbar">
				{authenticated && <TopNav location={this.props.location} />}
				{authenticated && <span className='team-name'><ActiveLink to="/team" teamId={teamIdParam}>{teamName}</ActiveLink></span>}
				{authenticated && isSuperuser && <span className='team-name'><ActiveLink to="/admin">Admin</ActiveLink></span>}
				{authenticated && <Button
					onClick={this.authenticate.bind(this)}
					title={authenticated ? "Log out" : "Sign in"}
				/>}
			</div>
		);
	}
}

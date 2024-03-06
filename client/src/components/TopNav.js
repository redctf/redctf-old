import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Route, Link } from "react-router-dom";
import ActiveLink from "./ui/ActiveLink";

@inject("store")
@observer
export default class TopNav extends Component {
	constructor(props) {
		super(props);
	}

	// authenticate(e) {
	// 	if (e) e.preventDefault();
	// 	this.props.store.authenticate();
	// }

	render() {
		return (
			<nav>
				<ActiveLink activeOnlyWhenExact={true} to="/">Nexus</ActiveLink>
				<ActiveLink to="/instructions">Protocol</ActiveLink>
				<ActiveLink to="/challenges">AI Encounters</ActiveLink>
				<ActiveLink to="/scoreboard">Metrics Matrix</ActiveLink>
			</nav>
		);
	}
}
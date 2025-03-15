import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Route, Link } from "react-router-dom";
import ActiveLink from "./ui/ActiveLink";
import K25 from '../images/k25.png'

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
				<ActiveLink activeOnlyWhenExact={true} to="/"><img src={K25} width="80"/></ActiveLink>
				<ActiveLink to="/instructions">Rules of the Road</ActiveLink>
				<ActiveLink to="/challenges">Race Tracks</ActiveLink>
				<ActiveLink to="/scoreboard">Podium</ActiveLink>
			</nav>
		);
	}
}
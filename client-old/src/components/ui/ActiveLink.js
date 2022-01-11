import React from "react";
import { Route, Link } from "react-router-dom";

const ActiveLink = ({ to, activeOnlyWhenExact, teamId, ...rest }) => (
	<Route
		path={to}
		exact={activeOnlyWhenExact}
		children={({ match }) => (
			<Link to={{pathname: to, search: teamId}} {...rest} className={match ? "active" : ""}/>
		)}
	/>
);

export default ActiveLink;


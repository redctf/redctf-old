import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Link } from "react-router-dom";

import DataWrapper from "../components/DataWrapper";
import Protected from "../components/Protected";

@DataWrapper
@Protected
@observer
export default class Subitem extends Component {

	// Solely an example of nested routes
	constructor(props) {
		super(props);
		this.store = this.props.store;
	}
	render() {
		const { item } = this.store.appState;
		return (
			<div className="page post">
				<Link to="/posts">← Back to Posts</Link>
				{!!item &&
					<article>
						<h1>{item.title}</h1>
						<p>{item.body}</p>
					</article>}

			</div>
		);
	}
}

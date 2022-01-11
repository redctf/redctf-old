import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import { Redirect } from "react-router-dom";

export default function DataWrapper(WrappedComponent) {
	@inject("store")
	@observer
	class DataFetcher extends Component {
		constructor(props) {
			super(props);
			this.store = this.props.store.appState;
		}

		componentDidMount() {
			console.log(this.props);
			let pathname = this.props.match.url;
			let id = this.props.match.id ? this.props.match.id : null;
		}

		componentWillUnmount() {
			this.store.clearItems();
		}

		render() {
			return <WrappedComponent {...this.props} />;
		}
	}
	return DataFetcher;
}

import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import Hero from './Hero';

@inject('store')
@observer
export default class Home extends Component {
	constructor(props) {
		super(props);
		this.store = this.props.store;
	}

	render() {
		const store = this.store;
		return (
			<div className={`page posts`}>
				<div className='instructions'>
					<h2>Kernelcon AI CTF</h2>
				</div>
			</div>
		);
	}
}

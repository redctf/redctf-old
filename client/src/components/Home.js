import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import Hero from './Hero';
import Fast from '../images/2fast2ctf.png';

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
			<div className='page home'>
				<Hero />
				<main>
					<img src={Fast} />
				</main>
			</div>
		);
	}
}

import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';

// import audioTMNT from '../audio/tmnt.mp3';

// import Hero from './Hero';

@inject('store')
@observer
export default class Home extends Component {
	constructor(props) {
		super(props);
		this.store = this.props.store;
	}

  componentDidMount() {
  }

	render() {
		const store = this.store;
		return (
			<div className='page home bkg-turt'>
        <h2 className='turts login-heading'>Kernelcon CTF</h2>

			</div>
		);
	}
}

import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';
import Hero from './Hero/Hero';

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
					<div className="section-header">
						<h3>A CTF Framework made with ReactJS, Mobx, RethinkDB, and Django.</h3>
						<hr />
					</div>
					<div className="section-item">
						<div className="section-logo react" />
						<div className="section-item-content">
							<a
								href="https://facebook.github.io/react/"
								target="_blank"
							>
								<h4>React</h4>
							</a>
							<small>UI Library</small>
							<p>
								React makes it painless to create
								{" "}
								<br />
								interactive UIs.
							</p>
						</div>
					</div>
					<div className="section-item">
						<div className="section-logo mobx" />
						<div className="section-item-content">
							<a
								href="http://mobxjs.github.io/mobx/"
								target="_blank"
							>
								<h4>MobX</h4>
							</a>
							<small>Reactive State Management</small>
							<p>
								MobX is a battle tested library that makes state management simple and scalable.
							</p>
						</div>
					</div>
					<div className="section-item">
						<div className="section-logo rethinkdb" />
						<div className="section-item-content">
							<a
								href="https://www.rethinkdb.com/"
								target="_blank"
							>
								<h4>RethinkDB</h4>
							</a>
							<small>Realtime Database</small>
							<p>
								RethinkDB is the open-source, scalable database that makes building realtime apps dramatically easier.
							</p>
						</div>
					</div>
					<div className="section-item">
						<div className="section-logo django" />
						<div className="section-item-content">
							<a
								href="https://www.djangoproject.com/"
								target="_blank"
							>
								<h4>Django</h4>
							</a>
							<small>High-level Python Web Framework</small>
							<p>
								Django is a Python Web framework that encourages rapid development and clean, pragmatic design. 
							</p>
						</div>
					</div>
				</main>
			</div>
		);
	}
}

import React, { Component } from 'react';
import { inject, observer } from 'mobx-react';

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
			<div className='page login'>
				<div className="kernelcon-ctf" />
				<div className='kernelcon-text'>A Virtual Experience for a Virtual Conference</div>


			  <div className={`page posts`}>
			    <div className='instructions'>
		        <div className='instruction-heading'>Basic Rules - check Instructions for more details.</div>
		        <ul>
		        	<li><b className='captain-morgan'>Maximum Four Team Members</b>
		        		<ul>
		        			<li className='johnny-walker'>
		        				Since this is an online only CTF, we can't monitor this technically.  However, we only have (4) Eternal Kernel Badges to award.
		        			</li>
		        		</ul>
		        	</li>
		        	<li><b className='captain-morgan'>Do Not Share Flags</b>
		        		<ul>
		        			<li className='johnny-walker'>
		        				Cheating is bad. We've isolated some challenges per user, with individuals flags. Consequences for getting caught results in disqualification.
		        			</li>
		        		</ul>
		        	</li>
		        	<li><b className='captain-morgan'>Report Issues or Bugs to Operations</b>
		        		<ul>
		        			<li className='johnny-walker'>
		        				We encourage fair play within reason. If you run into an issue, a bug, or a problem reach out to operations through discord <code>#kerneltron-ctf</code> channel or use the walk-up zoom meeting: <code>https://kernelcon.org/virtual/ctf</code>
		        			</li>
		        		</ul>
		        	</li>
		        </ul>
		      </div>
		    </div>
			</div>
		);
	}
}

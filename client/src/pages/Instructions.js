import React, { Component } from "react";

export default class Instructions extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {
    return (
      <div className={`page posts`}>
        <div className='instructions'>
          <h2>Hack the App Instructions</h2>

          <div className='instruction-heading'>Competition</div>
          <p>CTFs are...</p>

          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition schedule is from 10am to 4pm CST, Monday, February 5th, 2018.</p>

          <div className='instruction-sub-heading'>Flags</div>
          <p>Flag format is <code>{`CSGI{md5}`}</code>.  If you find an md5 hash, feel free to append the <code>{`CSGI{ }`}</code> around it and submit to see if you've identified a flag!</p>

          <div className='instruction-heading'>Resources</div>
          
          <div className='instruction-sub-heading'>CTF Resources</div>
          <p>The ctf resources are...</p>

          <div className='instruction-sub-heading'>Code Court Resources</div>
          <p>Click <a href="#" target="_blank">here</a> to view code court resources.</p>

          <div className='instruction-heading'>Contact Organizers</div>
          <p>Join us at the <a href="https://join.slack.com/t/hacktheapp/shared_invite/enQtMzA5MTcyMjM3ODI5LTkxMjhlZGZkNjllODI4ZmQ2MTQwNTVlOGVlYjgzOWI3NDA3M2IwZjEwOWQ0ZWQzMDE2NTQ1MjQ1ZjNkODI4NDM" target="_blank">hacktheapp slack.</a></p>


        </div>
      </div>
    );
  }
}

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
          <h2>Capture the Flag (CTF) Instructions</h2>

          <div className='instruction-heading'>Competition</div>
          <p>CTFs are competitions held in the cyber security community in which participants have to solve puzzles, break applications, reverse binaries, and find ways that challenges can be circumvented.  The goal of each challenge is to find a "flag" for points.  Often times the flags are hidden through several security flaws that the participants must exploit.</p>

          <p>When participating in a CTF, pay close attention to clues that may help tip you off to the aim of the challenge creator.  It is typical for challenge creators to hide clues in plain sight (e.g. the challenge title or description).  For example, the challenge may talk about and user and their financial PATH.  This would seem to indicate a Path Traversal vulnerability and it would be the first thing I would explore.</p>

          <p>Another common strategy is to solve easier challenges first and work to get points on the board as soon as possible.  CTFs are all scored differently, but tiebreakers usually go to the team who achieved that score first.  This particular CTF is a "Jeopardy CTF", meaning that challenges are divided into categories and the challenges are scored in accordance to their difficultly.  Still have questions or are new to CTFs?  Checkout our Resources area below for more information, including links to tools and strategy for solving CTF challenges.</p>

          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition is scheduled is from 8am (local time), Sunday, January 12th through Wednesday, January 15th.</p>

          <div className='instruction-sub-heading'>Flags</div>
          <p>Flag format is <code>{`contrast{md5}`}</code>.  If you find an md5 hash, feel free to append the <code>{`contrast{ }`}</code> around it and submit to see if you've identified a flag!</p>

          <div className='instruction-heading'>Resources</div>
          
          <div className='instruction-sub-heading'>CTF Resources</div>
          <p>The ctf resources are...</p>

          <div className='instruction-heading'>Contact Organizers</div>
          <p>Join us on slack in the #kickoff-ctf-2020 channel</p>


        </div>
      </div>
    );
  }
}

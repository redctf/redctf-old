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
          <h2>Kernelcon CTF Instructions</h2>
          <br/>
          <p>Capture the Flags (CTFs) are competitions held in the cyber security community in which participants have to solve puzzles, 
          break applications, reverse binaries, and find ways that challenges can be circumvented.  The goal of each 
          challenge is to find a "flag" for points.  Often times the flags are hidden through several security flaws 
          that the participants must exploit.</p>

          <br/>
          <p>When participating in a CTF, pay close attention to clues that may help tip you off to the aim of the 
          challenge creator.  It is typical for challenge creators to hide clues in plain sight (e.g. the challenge 
          title or description).  For example, the challenge may talk about a user and their financial PATH.  
          This potentially indicates a Path Traversal vulnerability and it would be the first thing to explore.</p>
          <br/>

          <p>Another common strategy is to solve easier challenges first and work to get points on the board as soon as 
          possible.  CTFs are all scored differently, but tiebreakers usually go to the team who achieved that score first.  
          This particular CTF is a "Jeopardy CTF", meaning that challenges are divided into categories and the challenges 
          are scored in accordance to their difficultly.  Still have questions or are new to CTFs?  Checkout our Resources 
          area below for more information, including links to tools and strategy for solving CTF challenges.</p>
          <br/>

          <p>Challenges will be inside the question blocks on the challenge page. The challenge's point value will be shown when you click on the challenge [?] block alongside the title and description of the challenge.</p>
          <br/>

          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition is scheduled is from 10am (CT), Friday, April 14th through 4pm (CT), Saturday, April 15th.</p>

          <div className='instruction-sub-heading'>Flags</div>

          <p>Flag format is <code>{`kernel{md5}`}</code>.  If you find an md5 hash, like <code>09f3ce6311494075c6ee0743a1bc3145</code>, please feel free to append the <code>{`kernel{ }`}</code> around it and submit to see if you've identified a flag! Some flags will be in plaintext so anything found within <code>{`kernel{plaintext_example_fake_flag}`}</code> could be a flag!</p>
          
          <div className='instruction-sub-heading'>HacKART</div>
          <p>HacKART is a new CTF challenge category this year which incorporates a physical component. You will need to request a HacKART block at the CTF host table at the front of the room. If you complete a HacKART challenge successfully one of the balloons attached to your HacKART block will pop just like in Mario Kart!</p>
          
          <div className='instruction-heading'>CTF Resources</div>
          <ul>
            <li><a href="https://ctfs.github.io/resources/" target="_blank" rel="noopener noreferrer">https://ctfs.github.io/resources/</a></li>
            <li><a href="https://github.com/ctfs/resources" target="_blank" rel="noopener noreferrer">https://github.com/ctfs/resources</a></li>
            <li><a href="https://apsdehal.in/awesome-ctf/" target="_blank" rel="noopener noreferrer">https://apsdehal.in/awesome-ctf/</a></li>
          </ul>

          <div className='instruction-heading'>Prizes</div>
          <p>The winning team will receive our coveted Eternal Kernel badge as well as a Nintendo Switch Lite!</p>
          <p>Several other prizes are available for participants as well! Winners MUST BE PRESENT to  claim their prize at the Own The Con closing ceremonies!</p>

          <div className='instruction-heading'>Contact Organizers</div>
          <p>Please visit us in the CTF room.</p>

        </div>
      </div>
    );
  }
}
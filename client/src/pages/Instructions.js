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
          <h2>Instructions</h2>
          <br /><p>Welcome to the Kernelcon: Arguably Insecure Jeopardy-style Capture the Flag (CTF) competition!</p><br /><br /> <p>Here are the instructions for participating:</p>






          <div className='instruction-heading'>Team Formation</div><p>Organize your team or participate individually. Each team can have a maximum of four members.
          </p><div className='instruction-heading'>Platform Access</div><p>Access the Kernelcon CTF platform provided for the competition. Ensure that your team has the necessary login credentials to access the challenges.
          </p><div className='instruction-heading'>Challenges Overview</div><p>Familiarize yourself with the categories of challenges available. These may include topics such as Cryptography, Reverse Engineering, Web Exploitation, Forensics, and more.
          </p><div className='instruction-heading'>Challenge Selection</div><p>Choose a challenge from the category board. Each challenge will have varying levels of difficulty indicated by point values.
          </p><div className='instruction-heading'>Problem Solving</div><p>Analyze the challenge description and associated files (if provided) to understand the nature of the problem. Apply your knowledge and skills to solve the challenge.
          </p><div className='instruction-heading'>Flag Submission</div><p>Once you've solved a challenge, submit the flag in the following format: kernel{`{<flag>}`}. Ensure the flag is correct and matches the format precisely.
          </p><div className='instruction-heading'>Scoring</div><p>Points are awarded based on the difficulty level of the challenge. The scoreboard will reflect your team's progress and ranking in real-time.
          </p><div className='instruction-heading'>Collaboration</div><p>Collaboration within your team is encouraged. Share insights, strategies, and techniques to solve challenges more efficiently.
          </p><div className='instruction-heading'>Fair Play</div><p>Follow ethical guidelines throughout the competition. Any form of cheating, such as sharing flags or using automated tools not allowed by the rules, will result in disqualification.
          </p><div className='instruction-heading'>Have Fun and Learn</div><p>Above all, enjoy the competition and seize the opportunity to learn new skills, techniques, and approaches to cybersecurity challenges.
          </p><div className='instruction-heading'>Prizes and Recognition</div><p>The winning team will be awarded our coveted Eternal Kernel badges, symbolizing their mastery in the Kernelcon: Arguably Insecure CTF. Additionally, each participant who successfully solves at least one challenge will be eligible for receiving a prize. Stay tuned for the announcement of prize details and distribution criteria.</p>

          <br />
          <div className='instruction-sub-heading'>Good luck, and may the best team emerge victorious in Kernelcon: Arguably Insecure CTF!</div>
          <div className='instruction-sub-heading'>Flags</div>

          <p>Flag format is <code>{`kernel{md5}`}</code>.  If you find an md5 hash, feel free to append the <code>{`kernel{ }`} </code> around it and submit to see if you've identified a flag! Badge challenges may not match this exact format.</p>
          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition is scheduled is from 8am (CT), Friday, April 4th through Saturday, April 5th at 2PM.</p>

        </div>
      </div>
    );
  }
}

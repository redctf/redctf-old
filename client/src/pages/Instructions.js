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

          <div className='instruction-heading'>🔥2Fast2CTF 🔥</div>
          <p>“It don’t matter if you hack by an inch or a mile—winning’s winning.”</p>

          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition is scheduled is from 10am (local time), Thursday, April 3rd through Friday, April  4th at 2:30 PM. </p>

          <div className='instruction-sub-heading'>🏁 START YOUR ENGINES! 🏁</div>

          <p>Welcome to 2Fast2CTF, the ultimate high-speed digital heist. This ain’t your grandma’s security drill—this is a full-throttle, no-holds-barred race through firewalls, exploits, and cryptographic mysteries. You’ve got skills? Time to prove it.</p>
          <p>If you find an md5 hash, feel free to append the kernel{ } around it and submit to see if you&#39;ve identified a flag! Badge challenges may not match this exact format.</p>

          <div className='instruction-sub-heading'>🚦 RULES OF THE ROAD 🚦</div>
          <p>
            <ol>
              <li>1️⃣ Respect the Streets (and Systems) – No attacking event infrastructure, no dirty tricks. We’re street racers, not script kiddies.</li>
              <li>2️⃣ Play Fair – No sharing flags, no cheating. We’re all in this together.</li>
              <li>3️⃣ NOS-Powered Hacking Only – All challenges are fair game, but if you try to brute-force your way through like a sledgehammer, you’re gonna crash.</li>
              <li>4️⃣ Stay in Your Lane – If it ain’t your system, don’t touch it. We break challenges, not laws.</li>
              <li>5️⃣ Flag or Be Flagged – Capture the flags <code>kernel{`{71bec39bdd997456a936ba93b9a7b531}`}</code>, submit them fast, and watch the leaderboard light up like a nitrous boost.</li>
            </ol>
          </p>
          <div className='instruction-sub-heading'>🏆 WINNERS TAKE ALL 🏆</div>
          <p>💰 Fastest Hackers Alive – First to capture a flag.</p>
          <p>🏆 Participation trophy - Everybody who has completed at least 1 challenge on their own will be entered into the drawing for the prize pool held at the end of the CTF. MUST BE PRESENT TO CLAIM TROPHY.</p>
          <p>🏁 First place prize - 4 eternal kernel badges and eternal bragging rights.</p>
          <div className='instruction-sub-heading'>💨 READY, SET, HACK! 💨</div>
          <p>You’re at the starting line. The clock’s ticking. The competition’s fierce. Will you be fast enough? Or will you get left in the digital dust?</p>
          <h3>🔥 HACK HARD. HACK FAST. HACK FURIOUS. 🔥</h3>


        </div>
      </div>
    );
  }
}
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

          <div className='instruction-heading'>🔥 2Fast2CTF INSTRUCTIONS 🔥</div>
          <p>“It don’t matter if you hack by an inch or a mile—winning’s winning.”</p>

          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition is scheduled is from 8am (local time), Sunday, January 12th through Wednesday, January 15th.</p>

          <div className='instruction-sub-heading'>🏁 START YOUR ENGINES! 🏁</div>

          <p>Welcome to 2Fast2CTF, the ultimate high-speed digital heist. This ain’t your grandma’s security drill—this is a full-throttle, no-holds-barred race through firewalls, exploits, and cryptographic mysteries. You’ve got skills? Time to prove it.</p>
          <p>If you find an md5 hash, feel free to append the kernel{ } around it and submit to see if you&#39;ve identified a flag! Badge challenges may not match this exact format.</p>

          <div className='instruction-heading'>🚦 RULES OF THE ROAD 🚦</div>
          <ol>
            <li>Respect the Streets (and Systems) – No attacking event infrastructure, no dirty tricks. We’re street racers, not script kiddies.</li>
            <li>It’s All About Family (and Ethics) – Work with your team, but keep it clean. No sabotage, no external help. No limit to team members, but only 4 Eterenal Kernels are awareded to a winning team.</li>
            <li>NOS-Powered Hacking Only – All challenges are fair game, but if you try to brute-force your way through like a sledgehammer, you’re gonna crash.</li>
            <li>Stay in Your Lane – If it ain’t your system, don’t touch it. We break challenges, not laws.</li>
            <li>Flag or Be Flagged – Capture the flags kernel{71bec39bdd997456a936ba93b9a7b531}, submit them fast, and watch the leaderboard light up like a nitrous boost.</li>
          </ol>
          <div className='instruction-sub-heading'>🏆 WINNERS TAKE ALL 🏆</div>
          <p>💰 Fastest Hackers Alive – First to capture a flag.</p>
          <p>🏆 Participation trophy - Everybody who has completed at least 1 challenge on their own will be entered into the drawing for the prize pool held at the end of the CTF. MUST BE PRESENT TO CLAIM TROPHY.</p>
          <p>🏁 First place prize - 4 eternal kernel badges and eternal bragging rights.</p>
          <div className='instruction-heading'>💨 READY, SET, HACK! 💨</div>
          <p>You’re at the starting line. The clock’s ticking. The competition’s fierce. Will you be fast enough? Or will you get left in the digital dust?</p>
          <h3>🔥 HACK HARD. HACK FAST. HACK FURIOUS. 🔥</h3>

        </div>
      </div>
    );
  }
}

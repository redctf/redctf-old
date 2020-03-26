import React, { Component } from "react";

export default class SpecialThanks extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
  }
  render() {
    return (
      <div className={`page posts`}>
        <div className='instructions'>
          <h2>Special Thanks</h2>

          <div className='instruction-heading'>Sponsors</div>
          <p>Capture the Flag events take time and resources to build. The Kerneltron CTF would not have been possible 
          without our kernelcon sponsors who supported us throughout our transition to a virtual conference.</p>

          <div className="main-section">
            <div className="section-item">
              <a className="section-logo securesky" x="f059" href="https://securesky.com/" target="_blank" rel="noopener noreferrer"/> {/**/}
            </div>
            <div className="section-item">
              <a className="section-logo splunk" x="aa87" href="https://www.splunk.com/" target="_blank" rel="noopener noreferrer"/>  {/**/}
            </div>
          </div>


          <div className='instruction-heading'>CTF Challenge Creators</div>
          <p>When we decided to move the conference, there was a mad scramble to recreate or re-theme challenges into our
          new CTF theme: TRON. Our volunteers spent hours crafted challenges that we hope will be extremely entertaining, 
          and above all educational. If you see them around the con, be sure to give them props or a hard time depending 
          on how your team is doing!</p>

          
          <div className='nari' x="39ae" /> {/**/}

          <div className='individuals'>
            <p x="69">Dan Amodio (@DanAmodio)</p> {/**/}
            <p x="f7">Matt Austin (@mattaustin)</p> {/**/}
            <p x="06">Michael Born (@Blu3Gl0w13)</p> {/**/}
            <p x="90">Dan Browder (@nevon)</p> {/**/}
            <p x="75">David Lindner (@golfhackerdave)</p> {/**/}
            <p x="79">Jacob Mohrbutter (Qu3b411)</p> {/**/}
            <p x="7d">Tyler Rosonke (@ZonkSec)</p> {/**/}
            <p x="c8">Adam Schaal (@clevernyyyy)</p> {/**/}
            <p x="30">Douglas Swartz</p> {/**/}
          </div>



          <div className='instruction-heading'>CTF Operations</div>
          <p>The individuals responsible for creating and maintaining this version of the redctf framework during the conference.</p>

          <br />
          <div className='individuals'>
            <p x="13">Jeris Rue (@elaboraterues)</p> {/**/}
            <p x="dontforget">Adam Schaal (@clevernyyyy)</p> {/**/}
            <p x="towrap">Nate Wood (@woodnsec)</p> {/**/}
          </div>

        </div>
      </div>
    );
  }
}

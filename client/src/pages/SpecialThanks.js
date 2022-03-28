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
          <p>Capture the Flag events take time and resources to build. The 2022 Kernelcon CTF would not have been possible 
          without our kernelcon sponsors who supported us.</p>

          <div className="main-section">
            <div className="section-item">
              <a className="section-logo checkpoint" href="https://www.checkpoint.com/" target="_blank" rel="noopener noreferrer"/>
            </div>
            <div className="section-item">
              <a className="section-logo protiviti" href="https://www.protiviti.com/" target="_blank" rel="noopener noreferrer"/>
            </div>
          </div>

          <br />
          <div className='instruction-heading'>CTF Challenge Creators</div>
          <p>Our volunteers spent hours crafting challenges that we hope will be extremely entertaining, 
          and above all educational. If you see them around the con, be sure to give them props or a hard time depending 
          on how your team is doing!</p>


          <br />
          <div className='individuals'>
            <p>Matt Austin (@mattaustin)</p> {/**/}
            <p>Jacob Mohrbutter (Qu3b411)</p> {/**/}
            <p>Tyler Rosonke (@ZonkSec)</p> {/**/}
            <p>Adam Schaal (@clevernyyyy)</p> {/**/}
            <p>Douglas Swartz</p> {/**/}
          </div>



          <br />
          <div className='instruction-heading'>CTF Operations</div>
          <p>The individuals responsible for creating and maintaining this version of the redctf framework during the conference.</p>

          <br />
          <div className='individuals'>
            <p>Nate Wood (@woodnsec)</p>
            <p>Jeris Rue (@elaboraterues)</p>
            <p>Adam Schaal (@clevernyyyy)</p>
          </div>

        </div>
      </div>
    );
  }
}
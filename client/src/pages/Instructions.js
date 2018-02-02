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
          <p>The competition will go from Xam to Xpm.</p>

          <div className='instruction-sub-heading'>Schedule</div>
          <p>The competition schedule is...</p>


          <div className='instruction-sub-heading'>Flags</div>
          <p>Flag format is <code>{`CSGI{md5}`}</code>.  If you find an md5 hash, feel free to append the <code>{`CSGI{ }`}</code> around it and submit to see if you've identified a flag!</p>




          <div className='instruction-heading'>Resources</div>
          <p>Resources</p>




          <div className='instruction-heading'>Contact Organizers</div>
          <p>Join us at hacktheapp slack: </p>










          <div>
           <ul>
              <li></li>
              <li>Competition goes from 10am - 4pm</li>
              <li>Resources List from email.</li>
            </ul> 


            https://www.cvedetails.com
            https://www.rapid7.com/db/vulnerabilities
            https://www.owasp.org/images/7/72/OWASP_Top_10-2017_%28en%29.pdf.pdf
            https://nvd.nist.gov/vuln/categories

            And for those who wanna try their hands at automators:
            https://cve.mitre.org/data/downloads/index.html


          </div>
        </div>
      </div>
    );
  }
}

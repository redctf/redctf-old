import React, { Component } from "react";
import { inject, observer } from "mobx-react";
import axios from "axios";

import Icon from "../../../components/ui/SvgIcon/Icon";
import AdminBox from './AdminBox';


@inject("store")
@observer
export default class Challenges extends Component {
  constructor(props) {
    super(props);
    this.store = this.props.store;
    this.state = {
      show: 'home'
    };
  }

  onUseFeature(ele) {
    this.setState({
      show: ele
    });

    this.props.parentCallback(true, 'challenges');
  }


  render() {
    return (
      <div className="page posts">
        <div className='admin-section'>

          {this.state.show === 'home' && 
            <div className='admin-box-section'>
              <div onClick={() => this.onUseFeature('edit')}>
                <AdminBox title='Edit Challenge' 
                  icon='EDIT'
                  viewBox='0 0 576 512'/>
              </div>

              <div onClick={() => this.onUseFeature('create')}>
                <AdminBox title='Create Challenge'
                  icon='LIST'
                  viewBox='0 0 512 512'/>
              </div>
            </div>
          }

          {this.state.show === 'edit' && 
            <div className='edit'>
              Edit
            </div>
          }

          {this.state.show === 'create' && 
            <div className='create'>
              Create Challenge
            </div>
          }
        </div>
      </div>
    );
  }
}

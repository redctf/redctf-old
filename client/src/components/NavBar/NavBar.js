import React from 'react';
import PropTypes from 'prop-types';
import './NavBar.scss';

export default function NavBar({ user }) {
  return (
    <div className='nav-bar'>
      <div className='nav-bar-container'>
        <div className='nav-bar-left'>
          <div className='nav-logo'>RedCTF</div>
        </div>  
        <div className='nav-bar-right'>
          <a className='nav-bar-right-item' href='/'>Home</a>
          <a className='nav-bar-right-item' href='/challenges'>Challenges</a>
          <a className='nav-bar-right-item' href='/redctf'>RedCTF</a>
          <span>{user.username}</span>
        </div>
      </div>
    </div>
  );
}

NavBar.propTypes = {
  user: PropTypes.object
};
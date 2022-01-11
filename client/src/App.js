import React, { useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

/* Import Pages */
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';

/* Import Styles */
import './App.scss';


function App() {
  const [token, setToken] = useState();

  if (!token) {
    return (
      <Login setToken={setToken} />
    );
  }

  // const [user, setUser] = useState();
  // const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <div className='wrapper'>
      <h1>Application</h1>
      <BrowserRouter>
        <Routes>
          <Route path='/home' element={<Home/>}/>
          <Route path='/login' element={<Login/>}/>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

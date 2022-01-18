import React, { useEffect } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

/* Import Hooks */
import useToken from './hooks/useToken';

/* Import Components */
import NavBar from './components/NavBar/NavBar';

/* Import Pages */
import Challenges from './pages/Challenges/Challenges';
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import RedCTF from './pages/RedCTF/RedCTF';

/* Import Styles */
import './styles/App.scss';

function App() {
  const { user, setUser } = useToken();

  useEffect(() => {
    document.documentElement.style.color = '#1a9e32';
  });

  if (!user) {
    return (
      <Login setUser={setUser} />
    );
  }

  return (
    <div className='app'>
      <NavBar user={user} />
      <div className='app-container'>
        <BrowserRouter>
          <Routes>
            <Route path='/' element={<Home/>}/>
            <Route path='/challenges' element={<Challenges/>}/>
            <Route path='/redctf' element={<RedCTF/>}/>
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;

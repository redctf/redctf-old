import React, { useEffect, createContext, useContext } from 'react';
import { inject, observer, Provider} from 'mobx-react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

/* Import Hooks */
import useToken from './hooks/useToken';
// import useUser from './hooks/useUser';

/* Import Components */
import NavBar from './components/NavBar/NavBar';

/* Import Pages */
import Challenges from './pages/Challenges/Challenges';
import Home from './pages/Home/Home';
import Login from './pages/Login/Login';
import RedCTF from './pages/RedCTF/RedCTF';

/* Import Styles */
import './styles/App.scss';

/* Import Stores */
import { AppState } from './stores/AppState';

const AppContext = createContext(new AppState());

function App() {
  // const { user, setUser } = useUser();
  const { token, setToken } = useToken();
  const TestStore = useContext(AppContext);

  console.log('TestStore: ', TestStore.token);

  useEffect(() => {
    document.documentElement.style.color = '#1a9e32';
  });

  if (!token) {
    return (
      <Login setToken={setToken} />
    );
  }

  return (
    <div className='app'>
      <NavBar />
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

export default (observer(()=> App()));

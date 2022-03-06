import { useState, createContext, useContext } from 'react';

/* Import Stores */
import { AppState } from '../stores/AppState';
const AppContext = createContext(new AppState());

export default function useToken() {
  const store = useContext(AppContext);

  const getToken = () => {
    const tokenString = sessionStorage.getItem('user');
    const userToken = JSON.parse(tokenString);
    console.log('userToken: ', userToken?.token);
    return userToken?.token
  };

  const [token, setToken] = useState(getToken());

  const saveToken = token => {
    sessionStorage.setItem('user', JSON.stringify(token));
    store.setToken(token);
    setToken(token);
  };

  return {
    setToken: saveToken,
    token
  }
}
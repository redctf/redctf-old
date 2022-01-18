import { useState } from 'react';

export default function useToken() {
  const getUser = () => {
    const tokenString = sessionStorage.getItem('token');
    const userToken = JSON.parse(tokenString);
    return userToken?.token
  };

  const [user, setUser] = useState(getUser());

  const saveUser = userToken => {
    sessionStorage.setItem('user', JSON.stringify(userToken));
    setUser(userToken);
  };

  return {
    setUser: saveUser,
    user
  }
}
// import { useState } from 'react';

// export default function useToken() {
//   const getUser = () => {
//     const userString = sessionStorage.getItem('user');
//     console.log('userString: ', userString);
//     const user = JSON.parse(userString);
//     return user
//   };

//   const [user, setUser] = useState(getUser());

//   const saveUser = user => {
//     sessionStorage.setItem('user', JSON.stringify(user));
//     setUser(user);
//   };

//   return {
//     setUser: saveUser,
//     user
//   }
// }
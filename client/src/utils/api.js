
// const myAxios = axios.create({
//   baseURL: 'http://localhost:5000/api/v1/',
//   headers: {
//     'Content-Type': 'application/json',
//     'Accept': 'application/json',
//   },
//   Authorization: `Bearer ${sessionStorage.getItem('token')}`,
// });

// myAxios.interceptors.response.use(
//   response => response,
//   error => {
//     if (error.response.status === 401) {
//       window.location.href = '/login';
//     }
//     return Promise.reject(error);
//   },
// );

// myAxios.interceptors.request.use(
//   config => {
//     config.headers.Authorization = `Bearer ${sessionStorage.getItem('token')}`;
//     return config;
//   },
//   error => Promise.reject(error),
// );



// export default myAxios;
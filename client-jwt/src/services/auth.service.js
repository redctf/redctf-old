import axios from "axios";
const API_URL = "/graphql/";
const BASE_URL = `${window.location.protocol}//${window.location.hostname}`;
const register = (username, email, password) => {
  return axios.post(API_URL + "signup", {
    username,
    email,
    password,
  });
};
const login = (username, password) => {
  const mut = `mutation {
    tokenAuth(username: "${username}", password: "${password}") {
      success
      errors
      token
      user {
        username
      }
    }
  }`;

  axios.defaults.baseURL = BASE_URL;
  axios.defaults.withCredentials = true;
  return axios
    .post(API_URL, {
      query: mut,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      if (response.data.accessToken) {
        localStorage.setItem("user", JSON.stringify(response.data));
      }
      return response.data;
    });
};
const logout = () => {
  localStorage.removeItem("user");
};
const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem("user"));
};
export default {
  register,
  login,
  logout,
  getCurrentUser,
};
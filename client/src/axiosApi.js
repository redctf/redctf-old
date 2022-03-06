import axios from 'axios'
const baseURL = `${window.location.protocol}//${window.location.hostname}`;
const jwt = JSON.parse(sessionStorage.getItem('user')) ? JSON.parse(sessionStorage.getItem('user')).token ? JSON.parse(sessionStorage.getItem('user')).token : null : null;

export default axios.create({
  baseURL: baseURL,
  timeout: 5000,
  headers: {
    'Authorization': "JWT " + jwt,
    'Content-Type': 'application/json',
    'accept': 'application/json'
  }
});

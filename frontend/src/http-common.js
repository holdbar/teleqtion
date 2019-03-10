import axios from 'axios'

const BASE_URL = 'http://localhost:8000/api/v1/';
export const LOGIN_URL = 'http://localhost:8000/login/';

// const token = localStorage.getItem('token');
const token = '8dc72581f7da420e36cf6b0da2da97a5c0971869';
// if (!token) {
//   window.location.replace(LOGIN_URL);
// }

export const HTTP = axios.create({
  baseURL: BASE_URL,
  headers: {
    Authorization: 'Token ' + token
  }
});

HTTP.interceptors.response.use(function (response) {
  return response
}, function (error) {
  if (error.response.status === 401) {
    window.location.replace(LOGIN_URL);
  }
  return Promise.reject(error)
});

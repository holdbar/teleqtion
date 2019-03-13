import axios from 'axios'

const BASE_URL = 'https://teleqtion.com/api/v1/';
export const LOGIN_URL = 'https://teleqtion.com/login/';
// const BASE_URL = 'http://localhost:8000/api/v1/';
// export const LOGIN_URL = 'http://localhost:8000/login/';

const token = localStorage.getItem('token');
// const token = '84008577a7cc4ef6188dca4e4ef7e3e0f8f48450';
if (!token) {
  window.location.replace(LOGIN_URL);
}

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

import axios from 'axios'

const BASE_URL = 'https://teleqtion.com/api/v1/';
export const LOGIN_URL = 'https://teleqtion.com/login/';
// const BASE_URL = 'http://localhost:8000/api/v1/';
// export const LOGIN_URL = 'http://localhost:8000/login/';

const token = localStorage.getItem('token');
// const token = '079f1afa0de07ec1d8abb7c2d7f09de1c59b9ebe';
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

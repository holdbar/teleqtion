import axios from 'axios'

// const token = localStorage.getItem('token');
const token = '8dc72581f7da420e36cf6b0da2da97a5c0971869';
if (!token) {
  window.location.replace("http://localhost:8000/login/");
}

export const HTTP = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  headers: {
    Authorization: 'Token ' + token
  }
});

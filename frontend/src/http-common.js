import axios from 'axios'

// const token = localStorage.getItem('token');
const token = '6658eafa62b2aef28421f12c99ceadfab1155a75';

export const HTTP = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  headers: {
    Authorization: 'Token ' + token
  }
});

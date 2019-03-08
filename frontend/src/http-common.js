import axios from 'axios'

// const token = localStorage.getItem('token');
const token = '53da78d6523ce1ac722232910ae164dd19dd0634';
if (!token) {
  window.location.replace("http://localhost:8000/login/");
}

export const HTTP = axios.create({
  baseURL: 'http://localhost:8000/api/v1/',
  headers: {
    Authorization: 'Token ' + token
  }
});

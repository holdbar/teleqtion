const url = 'http://localhost:8000/api/v1/';

const errors_div = document.querySelector('.errors');
const email_input = document.getElementById("email");
const password_input = document.getElementById("password");


function onSubmit() {
    axios.post(url + 'auth/login/', {
        email: email_input.value,
        password: password_input.value
    }).then(response => {
        if (response.status === 400) {
            errors_div.innerHTML = response.data.non_field_errors;
        } else {
            localStorage.setItem('token', response.data.key);
            window.location.href = "http://localhost:8081/";
        }
    }).catch(e => {
        errors_div.innerHTML = e.response.data.non_field_errors;
    });
    return false;
}

document.querySelector('form').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
document.querySelector('#submitBtn').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
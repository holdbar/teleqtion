const BASE_URL = window.location.protocol + "//" + window.location.host + "/" + 'api/v1/';

const success_div = document.querySelector('.success');
const errors_div = document.querySelector('.errors');
const email_input = document.getElementById("email");


function onSubmit() {
    axios.post(BASE_URL + 'auth/password/reset/', {
        email: email_input.value,
    }).then(response => {
        showSuccess(response.data.detail);
    }).catch(e => {
        showErrors(e.response.data);
    });
    return false;
}

function showErrors(data) {
    success_div.innerHTML = '';
    errors_div.innerHTML = data.non_field_errors;
}

function showSuccess(message) {
    success_div.innerHTML = message;
    errors_div.innerHTML = '';
}

document.querySelector('form').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
document.querySelector('#submitBtn').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
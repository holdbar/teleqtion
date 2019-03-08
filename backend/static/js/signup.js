const url = 'http://localhost:8000/api/v1/';

const success_div = document.querySelector('.success');
const errors_div = document.querySelector('.errors');
const email_input = document.getElementById("email");
const password_input = document.getElementById("password");
const email_errors_div = document.getElementById('email-errors');
const password_errors_div = document.getElementById('password-errors');

function onSubmit() {
    axios.post(url + 'registration/', {
        email: email_input.value,
        password: password_input.value
    }).then(response => {
        if (response.status === 201) {
            showSuccess(response.data.detail);
        } else {
            showErrors(response.data);
        }
    }).catch(e => {
        showErrors(e.response.data);
    });
    return false;
}

function showErrors(data) {
    success_div.innerHTML = '';
    if (data.hasOwnProperty('email')) {
        email_errors_div.innerHTML = getErrorHtml(data.email);
    }
    if (data.hasOwnProperty('password')) {
        password_errors_div.innerHTML = getErrorHtml(data.password);
    }
    if (data.hasOwnProperty('non_field_errors')) {
        errors_div.innerHTML = getErrorHtml(data.non_field_errors);
    }
}

function showSuccess(message) {
    success_div.innerHTML = message;
    email_errors_div.innerHTML = '';
    password_errors_div.innerHTML = '';
    errors_div.innerHTML = '';
}

function getErrorHtml(errors) {
    if (errors.length === 1) {
        return errors[0];
    }
    let list = '<ul>';
    for (let err of errors) {
        list += `<li>${err}</li>`;
    }
    list += '</ul>';
    return list;
}

document.querySelector('form').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
document.querySelector('#submitBtn').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
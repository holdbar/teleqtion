const BASE_URL = window.location.protocol + "//" + window.location.host + "/" + 'api/v1/';

const success_div = document.querySelector('.success');
const errors_div = document.querySelector('.errors');
const password1_input = document.getElementById('password1');
const password2_input = document.getElementById('password2');
const password1_errors_div = document.getElementById('password1-errors');
const password2_errors_div = document.getElementById('password2-errors');
const wait_div = document.querySelector('.wait');
const redirect_info_div = document.querySelector('.redirect');
const redirect_url = document.getElementById('redirect-url').value;
const uid = getUidFromUrl();
const token = getTokenFromUrl();

wait_div.style.display = 'none';


function getUidFromUrl() {
    let parts = window.location.pathname.split('/');
    return parts[parts.length - 3];
}

function getTokenFromUrl() {
    let parts = window.location.pathname.split('/');
    return parts[parts.length - 2];
}

function onSubmit() {
    if (!checkPasswordsMatch()) {
        showErrors({
            non_field_errors: `Passwords didn't match`,
        });
        return false;
    }

    wait_div.style.display = 'block';

    axios.post(BASE_URL + 'auth/password/reset/confirm/', {
        new_password1: password1_input.value,
        new_password2: password2_input.value,
        uid: uid,
        token: token
    }).then(response => {
        showSuccess(response.data.detail);
        redirectToLogin();
    }).catch(e => {
        showErrors(e.response.data);
    });
}

function checkPasswordsMatch() {
    return password1_input.value === password2_input.value;
}

function showErrors(data) {
    success_div.innerHTML = '';
    if (data.hasOwnProperty('new_password1')) {
        password1_errors_div.innerHTML = data.new_password1;
    }
    if (data.hasOwnProperty('new_password2')) {
        password2_errors_div.innerHTML = data.new_password2;
    }
    if (data.hasOwnProperty('non_field_errors')) {
        errors_div.innerHTML = data.non_field_errors;
    }
    if (data.hasOwnProperty('token') || data.hasOwnProperty('uid')) {
        errors_div.innerHTML = 'Invalid reset password link.';
    }
    wait_div.style.display = 'none';
}

function showSuccess(message) {
    success_div.innerHTML = message;
    password1_errors_div.innerHTML = '';
    password2_errors_div.innerHTML = '';
    errors_div.innerHTML = '';
    wait_div.style.display = 'none';
    redirect_info_div.style.display = 'block';
}

function redirectToLogin() {
    window.setTimeout(function () {
        window.location.href = redirect_url;
    }, 3000);
}

document.querySelector('form').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
document.querySelector('#submitBtn').onsubmit = function (e) {
    e.preventDefault();
    onSubmit();
};
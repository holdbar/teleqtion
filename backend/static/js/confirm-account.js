const BASE_URL = window.location.protocol + "//" + window.location.host + "/" + 'api/v1/';

const redirect_info_div = document.querySelector('.redirect');
const wait_div = document.querySelector('.wait');
const success_div = document.querySelector('.success');
const errors_div = document.querySelector('.errors');
const redirect_url = document.getElementById('redirect-url').value;
const confirmKey = getKeyFromUrl();

function getKeyFromUrl() {
    let parts = window.location.pathname.split('/');
    return parts[parts.length - 2];
}

function submitConfirmKey() {
    axios.post(BASE_URL + 'registration/verify-email/', {
        key: confirmKey
    }).then(response => {
        showSuccess();
        redirectToLogin();
    }).catch(e => {
        showErrors();
    });
}

function showSuccess() {
    success_div.innerHTML = 'Success!';
    wait_div.style.display = 'none';
    redirect_info_div.style.display = 'block';
}

function showErrors() {
    errors_div.innerHTML = 'Token is invalid.';
    wait_div.style.display = 'none';
}

function redirectToLogin() {
    window.setTimeout(function () {
        window.location.href = redirect_url;
    }, 3000);
}

submitConfirmKey();

document.addEventListener('DOMContentLoaded', () => {
    setInput('id_email', 'id_login', 'ВАША ПОЧТА', 'login-sign-up', 'sign-up');
    setInput('id_password1', 'id_pass', 'НОВЫЙ ПАРОЛЬ', 'pass-sign-up', 'sign-up');
    setInput('id_email', 'id_email', 'ВАШ ЛОГИН', 'login-sign-in', 'sign-in');
    setInput('id_password', 'id_password', 'ВАШ ПАРОЛЬ', 'pass-sign-in', 'sign-in');
});

function setInput(currId, newId, placeholder, className, method) {
    const input = document.getElementById(currId);
    input.id = newId;
    input.classList.add(className);
    input.placeholder = placeholder;
    input.autocomplete = 'on';
    input.oninput = () => highlightLink(method);
}
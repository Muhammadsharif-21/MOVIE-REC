function login() {
  const email = document.getElementById('login-email').value;
  const password = document.getElementById('login-password').value;

  fetch('/api/login', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: email, password: password })
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Login failed.');
        return;
      }
      window.location.href = '/';
    });
}
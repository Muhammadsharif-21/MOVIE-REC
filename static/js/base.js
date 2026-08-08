function refreshUserChip() {
  fetch('/api/me', { credentials: 'same-origin' })
    .then(response => response.json())
    .then(data => {
      const chip = document.getElementById('user-chip');
      if (!chip) return;
      if (data.logged_in) {
        chip.innerHTML = `${data.name} &nbsp; <button onclick="logout()">Logout</button>`;
      } else {
        chip.innerHTML = `<a href="/login" style="color: var(--gold); text-decoration: none;">Login</a>`;
      }
    });
}

function logout() {
  fetch('/api/logout', {
    method: 'POST',
    credentials: 'same-origin'
  })
    .then(response => response.json())
    .then(data => {
      window.location.href = '/login';
    });
}

function showToast(message, type = 'error') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 250);
  }, 3500);
}

refreshUserChip();
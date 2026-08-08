let currentPage = 1;

function nextPage() {
  currentPage++;
  loadShows();
}

function prevPage() {
  if (currentPage > 1) currentPage--;
  loadShows();
}

function loadShows() {
  const title = document.getElementById('search-title').value;
  const status = document.getElementById('filter-status').value;
  const sort = document.getElementById('sort-field').value;

  const params = new URLSearchParams();
  if (title) params.append('title', title);
  if (status) params.append('status', status);
  if (sort) params.append('sort', sort);
  params.append('page', currentPage);
  params.append('per_page', 6);

  document.getElementById('page-label').textContent = `Page ${currentPage}`;

  fetch(`/api/shows/?${params.toString()}`, { credentials: 'same-origin' })
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('shows-container');

      if (data.length === 0) {
        container.innerHTML = `<p class="empty-note">No shows match. Add one below.</p>`;
        return;
      }

      const html = data.map(show => `
<div class="stub">
  ${show.poster_url && show.poster_url !== 'N/A' ? `<img src="${show.poster_url}" alt="${show.title} poster" class="stub-poster">` : ''}
  <div class="stub-head">
    <h3 class="stub-title">${show.title}</h3>
    <div class="stub-meta">
      <span class="badge">${show.genre}</span>
      <span class="badge status-${show.status}">${show.status}</span>
      ${show.year && show.year !== 'N/A' ? `<span class="badge">${show.year}</span>` : ''}
    </div>
    ${show.plot && show.plot !== 'N/A' ? `<p class="stub-plot">${show.plot}</p>` : ''}
    <div class="stub-avg" id="avg-${show.id}"></div>
  </div>
  <div class="stub-body">
    <div class="edit-row">
      <input type="text" id="edit-title-${show.id}" value="${show.title}">
      <input type="text" id="edit-genre-${show.id}" value="${show.genre}">
      <input type="text" id="edit-status-${show.id}" value="${show.status}">
    </div>
    <div class="action-row">
      <button onclick="editShow(${show.id})">Save</button>
      <button class="danger" onclick="deleteShow(${show.id})">Delete</button>
    </div>

    <div class="reviews" id="reviews-${show.id}"></div>

    <div class="add-review-row">
      <input type="number" id="rating-input-${show.id}" placeholder="1-10">
      <input type="text" id="notes-input-${show.id}" placeholder="Notes">
      <button onclick="addReview(${show.id})">Add</button>
    </div>
  </div>
</div>
    `).join('');
      container.innerHTML = html;
      data.forEach(show => {
        loadReviews(show.id);
        loadStats(show.id);
      });
    });
}

function loadStats(showId) {
  fetch(`/api/shows/${showId}/stats`, { credentials: 'same-origin' })
    .then(response => response.json())
    .then(data => {
      const el = document.getElementById(`avg-${showId}`);
      if (!el) return;
      if (data.average_rating === null) {
        el.textContent = 'No ratings yet';
      } else {
        el.textContent = `Avg ${data.average_rating}/10`;
      }
    });
}

function addShow() {
  const title = document.getElementById('title-input').value;
  const genre = document.getElementById('genre-input').value;
  const status = document.getElementById('status-input').value;

  fetch('/api/shows/', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: title, genre: genre, status: status })
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Something went wrong adding this show.');
        return;
      }
      document.getElementById('title-input').value = '';
      document.getElementById('genre-input').value = '';
      document.getElementById('status-input').value = '';
      showToast('Show added', 'success');
      loadShows();
    });
}

function editShow(id) {
  const title = document.getElementById(`edit-title-${id}`).value;
  const genre = document.getElementById(`edit-genre-${id}`).value;
  const status = document.getElementById(`edit-status-${id}`).value;

  fetch(`/api/shows/${id}`, {
    method: 'PATCH',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: title, genre: genre, status: status })
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Could not update this show.');
        return;
      }
      showToast('Show updated', 'success');
      loadShows();
    });
}

function deleteShow(id) {
  fetch(`/api/shows/${id}`, {
    method: 'DELETE',
    credentials: 'same-origin'
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Could not delete this show.');
        return;
      }
      showToast('Show deleted', 'success');
      loadShows();
    });
}

function loadReviews(showId) {
  fetch(`/api/shows/${showId}/reviews`, { credentials: 'same-origin' })
    .then(response => response.json())
    .then(reviews => {
      const container = document.getElementById(`reviews-${showId}`);
      const html = reviews.map(review => `
      <div class="review">
        <span class="review-rating">${review.rating}/10</span>${review.notes}
        <div class="edit-row">
          <input type="number" id="edit-rating-${review.id}" value="${review.rating}">
          <input type="text" id="edit-notes-${review.id}" value="${review.notes}">
        </div>
        <div class="action-row">
          <button onclick="editReview(${review.id}, ${showId})">Save</button>
          <button class="danger" onclick="deleteReview(${review.id}, ${showId})">Delete</button>
        </div>
      </div>
    `).join('');
      container.innerHTML = html;
    });
}

function addReview(showId) {
  const rating = document.getElementById(`rating-input-${showId}`).value;
  const notes = document.getElementById(`notes-input-${showId}`).value;

  if (!rating) {
    showToast('Please enter a rating between 1 and 10.');
    return;
  }

  fetch(`/api/shows/${showId}/reviews`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ rating: parseInt(rating), notes: notes })
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Something went wrong adding this review.');
        return;
      }
      loadReviews(showId);
      loadStats(showId);
    });
}

function editReview(reviewId, showId) {
  const rating = document.getElementById(`edit-rating-${reviewId}`).value;
  const notes = document.getElementById(`edit-notes-${reviewId}`).value;

  fetch(`/api/reviews/${reviewId}`, {
    method: 'PATCH',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ rating: parseInt(rating), notes: notes })
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Could not update this review.');
        return;
      }
      loadReviews(showId);
      loadStats(showId);
    });
}

function deleteReview(reviewId, showId) {
  fetch(`/api/reviews/${reviewId}`, {
    method: 'DELETE',
    credentials: 'same-origin'
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Could not delete this review.');
        return;
      }
      loadReviews(showId);
      loadStats(showId);
    });
}

function resetMyShows() {
  if (!confirm('This deletes every show you own (and their reviews). Continue?')) return;

  fetch('/api/shows/reset', {
    method: 'DELETE',
    credentials: 'same-origin'
  })
    .then(response => response.json().then(data => ({ ok: response.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        showToast(data.message || 'Could not reset your shows.');
        return;
      }
      showToast('All your shows were cleared', 'success');
      loadShows();
    });
}

loadShows();
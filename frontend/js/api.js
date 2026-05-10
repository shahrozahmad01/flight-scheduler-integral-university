const BASE_URL = 'http://localhost:5000/api';

async function apiFetch(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || 'API request failed');
  }
  return data;
}

function showToast(message, type = 'success') {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.position = 'fixed';
  toast.style.bottom = '24px';
  toast.style.right = '24px';
  toast.style.padding = '14px 18px';
  toast.style.borderRadius = '12px';
  toast.style.color = 'white';
  toast.style.zIndex = 999;
  toast.style.background = type === 'error' ? '#b91c1c' : '#047857';
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

const API = {
  getFlights: (filters = {}) => {
    const params = new URLSearchParams(filters).toString();
    return apiFetch(`/flights/${params ? `?${params}` : ''}`);
  },
  getFlight: (id) => apiFetch(`/flights/${id}`),
  createFlight: (data) => apiFetch('/flights/', { method: 'POST', body: JSON.stringify(data) }),
  getFlightStats: () => apiFetch('/flights/stats/summary'),

  getPassengers: () => apiFetch('/passengers/'),
  getPassengerBookings: (id) => apiFetch(`/passengers/${id}/bookings`),

  getBookings: () => apiFetch('/bookings/'),
  createBooking: (data) => apiFetch('/bookings/', { method: 'POST', body: JSON.stringify(data) }),
  cancelBooking: (id) => apiFetch(`/bookings/${id}/cancel`, { method: 'PUT' }),

  getDisruptions: () => apiFetch('/disruptions/'),
  triggerDisruption: (data) => apiFetch('/disruptions/trigger', { method: 'POST', body: JSON.stringify(data) }),
  getAffectedPassengers: (id) => apiFetch(`/disruptions/${id}/affected`),
  getImpactAnalysis: (id) => apiFetch(`/disruptions/${id}/analysis`),
  resolveDisruption: (id) => apiFetch(`/disruptions/${id}/resolve`, { method: 'PUT' }),

  getRebookingOptions: (pid, fid) => apiFetch(`/rebook/options/${pid}/${fid}`),
  confirmRebooking: (data) => apiFetch('/rebook/confirm', { method: 'POST', body: JSON.stringify(data) }),
};

function showError(msg) { showToast(msg, 'error'); }
function showSuccess(msg) { showToast(msg, 'success'); }

window.API = API;
window.showError = showError;
window.showSuccess = showSuccess;

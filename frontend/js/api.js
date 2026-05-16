// Auto-detect API URL based on environment
// For local development, uses http://localhost:5000
// For production, set VITE_API_URL or use the deployed URL
const getBaseUrl = () => {
  const currentHost = window.location.hostname;
  const currentPort = window.location.port;
  
  // If running on localhost or 127.0.0.1, use local backend
  if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
    return `http://${currentHost}:5000/api`;
  }
  
  // For production, use the deployed backend
  // Update this URL to your production backend
  return 'https://flight-scheduler-backend.onrender.com/api';
};

const BASE_URL = getBaseUrl();

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
  // Flights API
  getFlights: (filters = {}) => {
    const params = new URLSearchParams(filters).toString();
    return apiFetch(`/flights/${params ? `?${params}` : ''}`);
  },
  getFlight: (id) => apiFetch(`/flights/${id}`),
  createFlight: (data) => apiFetch('/flights/', { method: 'POST', body: JSON.stringify(data) }),

  // Passengers API
  getPassengers: () => apiFetch('/passengers/'),
  getPassengerBookings: (id) => apiFetch(`/passengers/${id}/bookings`),

  // Bookings API
  getBookings: () => apiFetch('/bookings/'),
  createBooking: (data) => apiFetch('/bookings/', { method: 'POST', body: JSON.stringify(data) }),
  cancelBooking: (id) => apiFetch(`/bookings/${id}/cancel`, { method: 'PUT' }),
};

function showError(msg) { showToast(msg, 'error'); }
function showSuccess(msg) { showToast(msg, 'success'); }

window.API = API;
window.showError = showError;
window.showSuccess = showSuccess;

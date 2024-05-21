// src/services/csrfService.js

let csrfToken = '';

export async function fetchCsrfToken() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/csrf-token', {
      credentials: 'include'  // Ensure cookies are included
    });
    const data = await response.json();
    csrfToken = data.csrf_token;
    console.log(data)
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
  }
}

export function getCsrfToken() {
  return csrfToken;
}

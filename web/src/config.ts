export const APP_NAME = import.meta.env.VITE_APP_NAME || 'Attend';

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  import.meta.env.VITE_RUNTIME_API_FALLBACK ||
  'https://tekattend-api-772785199121.us-central1.run.app';

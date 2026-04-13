import { createTheme } from '@mui/material/styles';

export const appTheme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#0f172a' },
    secondary: { main: '#475569' },
    background: { default: '#f5f7fb', paper: '#ffffff' },
    success: { main: '#15803d' },
    warning: { main: '#d97706' },
    error: { main: '#b91c1c' },
  },
  shape: { borderRadius: 18 },
  typography: {
    fontFamily: ['Inter', 'Arial', 'sans-serif'].join(','),
    h1: { fontSize: '2.25rem', fontWeight: 700 },
    h2: { fontSize: '1.875rem', fontWeight: 700 },
    h3: { fontSize: '1.35rem', fontWeight: 700 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
});

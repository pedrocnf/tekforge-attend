import { useState } from 'react';
import { Box, Button, Card, CardContent, Container, Stack, TextField, Typography } from '@mui/material';
import { apiRequest } from '../api';

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError('');
    setMessage('');
    try {
      await apiRequest('/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });
      setMessage('Se o e-mail existir, a recuperação foi enviada.');
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <Box sx={{ minHeight: '100vh', py: 6, bgcolor: 'background.default' }}>
      <Container maxWidth="sm">
        <Card sx={{ borderRadius: 6 }}>
          <CardContent sx={{ p: 5 }}>
            <Typography variant="h2">Recuperar senha</Typography>
            <Typography color="text.secondary" sx={{ mt: 2, mb: 3 }}>
              Envie seu e-mail para começar a redefinição.
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
              <Stack spacing={2}>
                <TextField label="E-mail" value={email} onChange={(e) => setEmail(e.target.value)} />
                {message && <Typography color="success.main">{message}</Typography>}
                {error && <Typography color="error">{error}</Typography>}
                <Button type="submit" variant="contained">Enviar recuperação</Button>
              </Stack>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

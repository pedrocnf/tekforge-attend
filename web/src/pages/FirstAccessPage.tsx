import { useState } from 'react';
import { Box, Button, Card, CardContent, Container, Stack, TextField, Typography } from '@mui/material';
import { apiRequest } from '../api';

export function FirstAccessPage() {
  const [form, setForm] = useState({ email: '', new_password: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError('');
    setMessage('');
    try {
      await apiRequest('/auth/first-access', {
        method: 'POST',
        body: JSON.stringify(form),
      });
      setMessage('Primeiro acesso concluído. Verifique seu e-mail para validar a conta.');
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <Box sx={{ minHeight: '100vh', py: 6, bgcolor: 'background.default' }}>
      <Container maxWidth="sm">
        <Card sx={{ borderRadius: 6 }}>
          <CardContent sx={{ p: 5 }}>
            <Typography variant="h2">Primeiro acesso</Typography>
            <Typography color="text.secondary" sx={{ mt: 2, mb: 3 }}>
              Defina sua senha inicial e conclua a validação por e-mail.
            </Typography>
            <Box component="form" onSubmit={handleSubmit}>
              <Stack spacing={2}>
                <TextField label="E-mail" value={form.email} onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))} />
                <TextField label="Nova senha" type="password" value={form.new_password} onChange={(e) => setForm((p) => ({ ...p, new_password: e.target.value }))} />
                {message && <Typography color="success.main">{message}</Typography>}
                {error && <Typography color="error">{error}</Typography>}
                <Button type="submit" variant="contained">Concluir primeiro acesso</Button>
              </Stack>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

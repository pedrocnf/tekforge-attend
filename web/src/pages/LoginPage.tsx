import { useState } from 'react';
import { Box, Button, Card, CardContent, Container, Grid, Link, Stack, TextField, Typography } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export function LoginPage() {
  const [form, setForm] = useState({ username: 'admin', password: 'Sulaco2026' });
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    setError('');
    try {
      await login(form.username, form.password);
      navigate('/app');
    } catch (e: any) {
      setError(e.message);
    }
  }

  return (
    <Box sx={{ minHeight: '100vh', py: 6, bgcolor: 'background.default' }}>
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 6, height: '100%' }}>
              <CardContent sx={{ p: 5 }}>
                <Typography variant="body2" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1.8 }}>
                  Attend
                </Typography>
                <Typography variant="h2" sx={{ mt: 1 }}>Entre na sua área</Typography>
                <Typography color="text.secondary" sx={{ mt: 2 }}>
                  O navegador é o centro operacional do professor e da gestão. Aqui você organiza cadastros, abre a chamada e acompanha a fila.
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card sx={{ borderRadius: 6 }}>
              <CardContent sx={{ p: 5 }}>
                <Typography variant="h3" sx={{ mb: 3 }}>Login</Typography>
                <Box component="form" onSubmit={handleSubmit}>
                  <Stack spacing={2}>
                    <TextField label="Usuário" value={form.username} onChange={(e) => setForm((p) => ({ ...p, username: e.target.value }))} />
                    <TextField label="Senha" type="password" value={form.password} onChange={(e) => setForm((p) => ({ ...p, password: e.target.value }))} />
                    {error && <Typography color="error">{error}</Typography>}
                    <Button type="submit" variant="contained" size="large">Entrar</Button>
                    <Stack direction="row" justifyContent="space-between">
                      <Link component={RouterLink} to="/first-access" underline="hover">Primeiro acesso?</Link>
                      <Link component={RouterLink} to="/forgot-password" underline="hover">Recuperar senha</Link>
                    </Stack>
                  </Stack>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

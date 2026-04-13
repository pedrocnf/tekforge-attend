import { Card, CardContent, Grid, Stack, Typography } from '@mui/material';
import { useAuth } from '../context/AuthContext';

export function DashboardPage() {
  const { user } = useAuth();
  const cards = [
    { label: 'Módulo central', value: 'Cadastros' },
    { label: 'Operação crítica', value: 'Chamada' },
    { label: 'Segurança', value: 'Validação por e-mail' },
    { label: 'Experiência', value: 'Fluxo guiado' },
  ];

  return (
    <Stack spacing={3}>
      <Card sx={{ borderRadius: 6 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="body2" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1.8 }}>
            Painel principal
          </Typography>
          <Typography variant="h2" sx={{ mt: 1 }}>
            Olá, {user?.full_name}
          </Typography>
          <Typography color="text.secondary" sx={{ mt: 2, maxWidth: 920 }}>
            Agora, organize a estrutura acadêmica, cadastre alunos, confirme matrículas e abra a chamada para acompanhar a presença em tempo real.
          </Typography>
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {cards.map((card) => (
          <Grid item xs={12} md={6} xl={3} key={card.label}>
            <Card sx={{ borderRadius: 5 }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="body2" color="text.secondary">{card.label}</Typography>
                <Typography variant="h3" sx={{ mt: 1 }}>{card.value}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}

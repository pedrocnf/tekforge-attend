import { Box, Button, Card, CardContent, Container, Grid, Stack, Typography } from '@mui/material';
import ArrowForwardRoundedIcon from '@mui/icons-material/ArrowForwardRounded';
import { Link as RouterLink } from 'react-router-dom';

export function HomePage() {
  const cards = [
    {
      title: 'SOU PROFESSOR',
      description: 'Cadastros, matrícula, abertura de chamada e fila de confirmação em tempo real.',
    },
    {
      title: 'SOU ALUNO',
      description: 'Primeiro acesso, recuperação de senha e experiência acadêmica no ecossistema Attend.',
    },
  ];

  return (
    <Box sx={{ minHeight: '100vh', py: 6, bgcolor: 'background.default' }}>
      <Container maxWidth="lg">
        <Card sx={{ borderRadius: 6, mb: 4 }}>
          <CardContent sx={{ p: { xs: 3, md: 5 } }}>
            <Typography variant="body2" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1.8 }}>
              Tekforge ecosystem
            </Typography>
            <Typography variant="h1" sx={{ mt: 1 }}>Attend</Typography>
            <Typography variant="h6" color="text.secondary" sx={{ mt: 2, maxWidth: 860, fontWeight: 400 }}>
              Presença acadêmica inteligente com base institucional, cadastros centralizados, validação por e-mail,
              importação Excel e fila de chamada guiada para o professor.
            </Typography>
          </CardContent>
        </Card>

        <Grid container spacing={3}>
          {cards.map((card) => (
            <Grid item xs={12} md={6} key={card.title}>
              <Card sx={{ borderRadius: 6, height: '100%' }}>
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h3">{card.title}</Typography>
                  <Typography color="text.secondary" sx={{ mt: 2, mb: 4 }}>
                    {card.description}
                  </Typography>
                  <Button component={RouterLink} to="/login" variant="contained" endIcon={<ArrowForwardRoundedIcon />}>
                    Continuar
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Stack direction="row" justifyContent="flex-end" sx={{ mt: 4 }}>
          <Button component={RouterLink} to="/login" color="secondary">
            GESTÃO DA APLICAÇÃO
          </Button>
        </Stack>
      </Container>
    </Box>
  );
}

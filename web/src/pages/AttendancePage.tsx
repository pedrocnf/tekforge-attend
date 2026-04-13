import WarningAmberRoundedIcon from '@mui/icons-material/WarningAmberRounded';
import { Box, Button, Chip, Grid, MenuItem, Stack, TextField, Typography } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { SectionCard } from '../components/SectionCard';
import { useAuth } from '../context/AuthContext';
import type { AttendanceEvent, AttendanceRequest, Discipline } from '../types';

const initialForm = { discipline_id: '', title: '', lesson_date: '', lesson_time: '', allow_remote_requests: true };

export function AttendancePage() {
  const { token } = useAuth();
  const [disciplines, setDisciplines] = useState<Discipline[]>([]);
  const [events, setEvents] = useState<AttendanceEvent[]>([]);
  const [requests, setRequests] = useState<AttendanceRequest[]>([]);
  const [selectedEventId, setSelectedEventId] = useState('');
  const [form, setForm] = useState(initialForm);
  const [confirm, setConfirm] = useState<{ open: boolean; title: string; action: null | (() => Promise<void>) }>({ open: false, title: '', action: null });

  async function loadAll() {
    const [disciplinesRows, eventsRows] = await Promise.all([
      apiRequest<Discipline[]>('/disciplines', {}, token),
      apiRequest<AttendanceEvent[]>('/attendance/events', {}, token),
    ]);
    setDisciplines(disciplinesRows);
    setEvents(eventsRows);
    if (!selectedEventId && eventsRows.length) setSelectedEventId(eventsRows[0].id);
  }

  async function loadRequests(eventId: string) {
    setRequests(await apiRequest<AttendanceRequest[]>(`/attendance/events/${eventId}/requests`, {}, token));
  }

  useEffect(() => { loadAll().catch(console.error); }, []);
  useEffect(() => { if (selectedEventId) loadRequests(selectedEventId).catch(console.error); }, [selectedEventId]);

  async function createEvent() {
    const ev = await apiRequest<AttendanceEvent>('/attendance/events', { method: 'POST', body: JSON.stringify(form) }, token);
    setForm(initialForm);
    await loadAll();
    setSelectedEventId(ev.id);
    setConfirm({ open: false, title: '', action: null });
  }

  async function reviewRequest(requestId: string, status: 'confirmed' | 'denied') {
    await apiRequest(`/attendance/requests/${requestId}/review`, { method: 'POST', body: JSON.stringify({ status }) }, token);
    if (selectedEventId) await loadRequests(selectedEventId);
    setConfirm({ open: false, title: '', action: null });
  }

  async function closeEvent(eventId: string) {
    await apiRequest(`/attendance/events/${eventId}/close`, { method: 'POST' }, token);
    await loadAll();
    if (selectedEventId) await loadRequests(selectedEventId);
    setConfirm({ open: false, title: '', action: null });
  }

  const columns = useMemo<GridColDef<AttendanceRequest>[]>(() => [
    { field: 'student_user_id', headerName: 'Aluno', flex: 1, minWidth: 200 },
    { field: 'channel', headerName: 'Canal', width: 120 },
    { field: 'status', headerName: 'Status', width: 130 },
    { field: 'stars', headerName: 'Estrelas', width: 110 },
    {
      field: 'warning_distance',
      headerName: 'Alerta 100m',
      width: 150,
      renderCell: (params) => params.value ? <Chip icon={<WarningAmberRoundedIcon />} label="Alerta" color="warning" /> : <Chip label="OK" color="success" />
    },
    {
      field: 'actions',
      headerName: 'Ações',
      width: 250,
      sortable: false,
      filterable: false,
      renderCell: (params) => (
        <Stack direction="row" spacing={1}>
          <Button size="small" variant="contained" color="success" onClick={() => setConfirm({ open: true, title: 'Confirmar presença do aluno?', action: async () => reviewRequest(params.row.id, 'confirmed') })}>Aceitar</Button>
          <Button size="small" variant="outlined" color="error" onClick={() => setConfirm({ open: true, title: 'Recusar solicitação do aluno?', action: async () => reviewRequest(params.row.id, 'denied') })}>Recusar</Button>
        </Stack>
      )
    }
  ], []);

  return (
    <Stack spacing={3}>
      <SectionCard title="Abrir chamada" action={<Button variant="contained" onClick={() => setConfirm({ open: true, title: 'Deseja abrir a chamada agora?', action: createEvent })}>Abrir chamada</Button>}>
        <Typography color="text.secondary" sx={{ mb: 2 }}>
          Agora, posicione-se e abra a chamada para que os alunos possam te encontrar.
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField select label="Disciplina" fullWidth value={form.discipline_id} onChange={(e) => setForm((p) => ({ ...p, discipline_id: e.target.value }))}>
              {disciplines.map((d) => <MenuItem key={d.id} value={d.id}>{d.name}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12} md={6}><TextField label="Título da aula" fullWidth value={form.title} onChange={(e) => setForm((p) => ({ ...p, title: e.target.value }))} /></Grid>
          <Grid item xs={12} md={6}><TextField label="Data" fullWidth value={form.lesson_date} onChange={(e) => setForm((p) => ({ ...p, lesson_date: e.target.value }))} placeholder="2026-04-12" /></Grid>
          <Grid item xs={12} md={6}><TextField label="Horário" fullWidth value={form.lesson_time} onChange={(e) => setForm((p) => ({ ...p, lesson_time: e.target.value }))} placeholder="19:00" /></Grid>
        </Grid>
      </SectionCard>

      <SectionCard title="Chamadas criadas">
        <Stack spacing={1.5}>
          {events.map((event) => (
            <Box key={event.id} sx={{ p: 2, border: '1px solid', borderColor: selectedEventId === event.id ? 'primary.main' : 'divider', borderRadius: 4, display: 'flex', justifyContent: 'space-between', gap: 2 }}>
              <Box sx={{ cursor: 'pointer' }} onClick={() => setSelectedEventId(event.id)}>
                <Typography fontWeight={700}>{event.title}</Typography>
                <Typography variant="body2" color="text.secondary">{event.lesson_date} · {event.lesson_time}</Typography>
              </Box>
              <Stack direction="row" spacing={1}>
                <Chip label={event.status} color={String(event.status).toLowerCase() === 'open' ? 'success' : 'default'} />
                {String(event.status).toLowerCase() === 'open' && <Button variant="outlined" color="error" onClick={() => setConfirm({ open: true, title: 'Deseja encerrar a chamada agora?', action: async () => closeEvent(event.id) })}>Fechar</Button>}
              </Stack>
            </Box>
          ))}
        </Stack>
      </SectionCard>

      <SectionCard title="Fila em tempo real">
        <Typography color="text.secondary" sx={{ mb: 2 }}>
          Solicitações acima de 100 metros aparecem com alerta visual para decisão do professor.
        </Typography>
        <Box sx={{ height: 520 }}>
          <DataGrid rows={requests} columns={columns} pageSizeOptions={[10, 20, 50]} />
        </Box>
      </SectionCard>

      <ConfirmDialog open={confirm.open} title="Confirmar ação" message={confirm.title} onCancel={() => setConfirm({ open: false, title: '', action: null })} onConfirm={() => confirm.action?.().catch(console.error)} />
    </Stack>
  );
}

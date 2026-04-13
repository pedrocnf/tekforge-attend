import AddRoundedIcon from '@mui/icons-material/AddRounded';
import { Box, Button, Grid, MenuItem, Stack, TextField } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { SectionCard } from '../components/SectionCard';
import { useAuth } from '../context/AuthContext';
import type { Discipline, Institution } from '../types';

const initialForm = {
  name: '',
  institution_id: '',
  semester: '',
  academic_shift: '',
  period_label: '',
  weekly_meetings: [{ weekday: 'Segunda', start_time: '19:00', end_time: '20:40' }],
  total_workload_hours: 60,
  weekly_lessons_count: 2,
  lesson_duration_minutes: 100,
};

export function DisciplinesPage() {
  const { token } = useAuth();
  const [rows, setRows] = useState<Discipline[]>([]);
  const [institutions, setInstitutions] = useState<Institution[]>([]);
  const [form, setForm] = useState(initialForm);
  const [confirmOpen, setConfirmOpen] = useState(false);

  async function loadAll() {
    const [disciplines, insts] = await Promise.all([
      apiRequest<Discipline[]>('/disciplines', {}, token),
      apiRequest<Institution[]>('/institutions', {}, token),
    ]);
    setRows(disciplines);
    setInstitutions(insts);
  }

  useEffect(() => { loadAll().catch(console.error); }, []);

  async function createItem() {
    await apiRequest('/disciplines', { method: 'POST', body: JSON.stringify(form) }, token);
    setForm(initialForm);
    await loadAll();
    setConfirmOpen(false);
  }

  const columns = useMemo<GridColDef<Discipline>[]>(() => [
    { field: 'name', headerName: 'Disciplina', flex: 1.1, minWidth: 220 },
    { field: 'semester', headerName: 'Semestre', width: 140 },
    { field: 'period_label', headerName: 'Período', width: 150 },
    { field: 'academic_shift', headerName: 'Turno', width: 150 },
    { field: 'weekly_lessons_count', headerName: 'Aulas/semana', width: 140 },
  ], []);

  return (
    <Stack spacing={3}>
      <SectionCard title="Disciplinas" action={<Button startIcon={<AddRoundedIcon />} variant="contained" onClick={() => setConfirmOpen(true)}>Salvar disciplina</Button>}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}><TextField label="Nome da disciplina" fullWidth value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} /></Grid>
          <Grid item xs={12} md={6}>
            <TextField select label="Instituição" fullWidth value={form.institution_id} onChange={(e) => setForm((p) => ({ ...p, institution_id: e.target.value }))}>
              {institutions.map((i) => <MenuItem key={i.id} value={i.id}>{i.name}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12} md={4}><TextField label="Semestre" fullWidth value={form.semester} onChange={(e) => setForm((p) => ({ ...p, semester: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Turno acadêmico" fullWidth value={form.academic_shift} onChange={(e) => setForm((p) => ({ ...p, academic_shift: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Período" fullWidth value={form.period_label} onChange={(e) => setForm((p) => ({ ...p, period_label: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Dia da semana" fullWidth value={form.weekly_meetings[0].weekday} onChange={(e) => setForm((p) => ({ ...p, weekly_meetings: [{ ...p.weekly_meetings[0], weekday: e.target.value }] }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Hora início" fullWidth value={form.weekly_meetings[0].start_time} onChange={(e) => setForm((p) => ({ ...p, weekly_meetings: [{ ...p.weekly_meetings[0], start_time: e.target.value }] }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Hora fim" fullWidth value={form.weekly_meetings[0].end_time} onChange={(e) => setForm((p) => ({ ...p, weekly_meetings: [{ ...p.weekly_meetings[0], end_time: e.target.value }] }))} /></Grid>
          <Grid item xs={12} md={4}><TextField type="number" label="Carga horária total" fullWidth value={form.total_workload_hours} onChange={(e) => setForm((p) => ({ ...p, total_workload_hours: Number(e.target.value) }))} /></Grid>
          <Grid item xs={12} md={4}><TextField type="number" label="Aulas semanais" fullWidth value={form.weekly_lessons_count} onChange={(e) => setForm((p) => ({ ...p, weekly_lessons_count: Number(e.target.value) }))} /></Grid>
          <Grid item xs={12} md={4}><TextField type="number" label="Duração (min)" fullWidth value={form.lesson_duration_minutes} onChange={(e) => setForm((p) => ({ ...p, lesson_duration_minutes: Number(e.target.value) }))} /></Grid>
        </Grid>
      </SectionCard>
      <SectionCard title="Base cadastrada">
        <Box sx={{ height: 480 }}><DataGrid rows={rows} columns={columns} pageSizeOptions={[10, 20, 50]} /></Box>
      </SectionCard>
      <ConfirmDialog open={confirmOpen} title="Confirmar cadastro" message="Deseja confirmar o cadastro da disciplina?" onCancel={() => setConfirmOpen(false)} onConfirm={() => createItem().catch(console.error)} />
    </Stack>
  );
}

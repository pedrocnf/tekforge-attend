import AddRoundedIcon from '@mui/icons-material/AddRounded';
import { Box, Button, Grid, MenuItem, Stack, TextField } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { SectionCard } from '../components/SectionCard';
import { useAuth } from '../context/AuthContext';
import type { Discipline, Enrollment, Student } from '../types';

const initialForm = { student_user_id: '', discipline_id: '' };

export function EnrollmentsPage() {
  const { token } = useAuth();
  const [rows, setRows] = useState<Enrollment[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [disciplines, setDisciplines] = useState<Discipline[]>([]);
  const [form, setForm] = useState(initialForm);
  const [confirmOpen, setConfirmOpen] = useState(false);

  async function loadAll() {
    const [enrollments, studentsRows, disciplinesRows] = await Promise.all([
      apiRequest<Enrollment[]>('/enrollments', {}, token),
      apiRequest<Student[]>('/students', {}, token),
      apiRequest<Discipline[]>('/disciplines', {}, token),
    ]);
    setRows(enrollments);
    setStudents(studentsRows);
    setDisciplines(disciplinesRows);
  }

  useEffect(() => { loadAll().catch(console.error); }, []);

  async function createItem() {
    await apiRequest('/enrollments', { method: 'POST', body: JSON.stringify(form) }, token);
    setForm(initialForm);
    await loadAll();
    setConfirmOpen(false);
  }

  const columns = useMemo<GridColDef<Enrollment>[]>(() => [
    { field: 'student_user_id', headerName: 'Aluno (user_id)', flex: 1, minWidth: 220 },
    { field: 'discipline_id', headerName: 'Disciplina (id)', flex: 1, minWidth: 220 },
    { field: 'is_active', headerName: 'Ativa', width: 100, type: 'boolean' },
    { field: 'created_at', headerName: 'Criada em', width: 200 },
  ], []);

  return (
    <Stack spacing={3}>
      <SectionCard title="Matrículas" action={<Button startIcon={<AddRoundedIcon />} variant="contained" onClick={() => setConfirmOpen(true)}>Salvar matrícula</Button>}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <TextField select label="Aluno" fullWidth value={form.student_user_id} onChange={(e) => setForm((p) => ({ ...p, student_user_id: e.target.value }))}>
              {students.map((s) => <MenuItem key={s.id} value={s.user_id}>{s.full_name}</MenuItem>)}
            </TextField>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField select label="Disciplina" fullWidth value={form.discipline_id} onChange={(e) => setForm((p) => ({ ...p, discipline_id: e.target.value }))}>
              {disciplines.map((d) => <MenuItem key={d.id} value={d.id}>{d.name}</MenuItem>)}
            </TextField>
          </Grid>
        </Grid>
      </SectionCard>
      <SectionCard title="Base cadastrada">
        <Box sx={{ height: 480 }}><DataGrid rows={rows} columns={columns} pageSizeOptions={[10, 20, 50]} /></Box>
      </SectionCard>
      <ConfirmDialog open={confirmOpen} title="Confirmar matrícula" message="Deseja confirmar a matrícula do aluno na disciplina?" onCancel={() => setConfirmOpen(false)} onConfirm={() => createItem().catch(console.error)} />
    </Stack>
  );
}

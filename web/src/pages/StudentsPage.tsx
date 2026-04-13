import AddRoundedIcon from '@mui/icons-material/AddRounded';
import UploadFileRoundedIcon from '@mui/icons-material/UploadFileRounded';
import { Box, Button, FormControlLabel, Grid, Stack, Switch, TextField } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { SectionCard } from '../components/SectionCard';
import { useAuth } from '../context/AuthContext';
import type { Student } from '../types';

const initialForm = { full_name: '', class_name: '', cpf: '', email: '', phone: '', username: '', send_email: true };

export function StudentsPage() {
  const { token } = useAuth();
  const [rows, setRows] = useState<Student[]>([]);
  const [form, setForm] = useState(initialForm);
  const [importFile, setImportFile] = useState<File | null>(null);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [importConfirmOpen, setImportConfirmOpen] = useState(false);

  async function loadRows() {
    setRows(await apiRequest<Student[]>('/students', {}, token));
  }

  useEffect(() => { loadRows().catch(console.error); }, []);

  async function createItem() {
    await apiRequest('/students', { method: 'POST', body: JSON.stringify(form) }, token);
    setForm(initialForm);
    await loadRows();
    setConfirmOpen(false);
  }

  async function importItems() {
    if (!importFile) return;
    const fd = new FormData();
    fd.append('file', importFile);
    await apiRequest('/students/import', { method: 'POST', body: fd }, token);
    await loadRows();
    setImportFile(null);
    setImportConfirmOpen(false);
  }

  const columns = useMemo<GridColDef<Student>[]>(() => [
    { field: 'full_name', headerName: 'Aluno', flex: 1.1, minWidth: 220 },
    { field: 'class_name', headerName: 'Turma', width: 180 },
    { field: 'cpf', headerName: 'CPF', width: 160 },
    { field: 'email', headerName: 'E-mail', flex: 1, minWidth: 240 },
    { field: 'phone', headerName: 'Telefone', width: 160 },
  ], []);

  return (
    <Stack spacing={3}>
      <SectionCard title="Alunos" action={
        <Stack direction="row" spacing={1}>
          <Button startIcon={<UploadFileRoundedIcon />} variant="outlined" onClick={() => importFile && setImportConfirmOpen(true)}>Importar Excel</Button>
          <Button startIcon={<AddRoundedIcon />} variant="contained" onClick={() => setConfirmOpen(true)}>Salvar aluno</Button>
        </Stack>
      }>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}><TextField label="Nome completo" fullWidth value={form.full_name} onChange={(e) => setForm((p) => ({ ...p, full_name: e.target.value }))} /></Grid>
          <Grid item xs={12} md={6}><TextField label="Turma" fullWidth value={form.class_name} onChange={(e) => setForm((p) => ({ ...p, class_name: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="CPF" fullWidth value={form.cpf} onChange={(e) => setForm((p) => ({ ...p, cpf: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Telefone" fullWidth value={form.phone} onChange={(e) => setForm((p) => ({ ...p, phone: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Username" fullWidth value={form.username} onChange={(e) => setForm((p) => ({ ...p, username: e.target.value }))} /></Grid>
          <Grid item xs={12} md={8}><TextField label="E-mail" fullWidth value={form.email} onChange={(e) => setForm((p) => ({ ...p, email: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><FormControlLabel control={<Switch checked={form.send_email} onChange={(e) => setForm((p) => ({ ...p, send_email: e.target.checked }))} />} label="Enviar e-mail" sx={{ mt: 1 }} /></Grid>
          <Grid item xs={12}>
            <Button component="label" variant="outlined">
              Selecionar planilha Excel
              <input hidden type="file" accept=".xlsx" onChange={(e) => setImportFile(e.target.files?.[0] || null)} />
            </Button>
          </Grid>
        </Grid>
      </SectionCard>
      <SectionCard title="Base cadastrada">
        <Box sx={{ height: 480 }}><DataGrid rows={rows} columns={columns} pageSizeOptions={[10, 20, 50]} /></Box>
      </SectionCard>
      <ConfirmDialog open={confirmOpen} title="Confirmar cadastro" message="Deseja confirmar o cadastro do aluno?" onCancel={() => setConfirmOpen(false)} onConfirm={() => createItem().catch(console.error)} />
      <ConfirmDialog open={importConfirmOpen} title="Confirmar importação" message="Deseja importar a planilha de alunos?" onCancel={() => setImportConfirmOpen(false)} onConfirm={() => importItems().catch(console.error)} />
    </Stack>
  );
}

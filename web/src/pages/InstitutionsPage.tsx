import AddRoundedIcon from '@mui/icons-material/AddRounded';
import { Box, Button, Grid, Stack, TextField } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { useEffect, useMemo, useState } from 'react';
import { apiRequest } from '../api';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { SectionCard } from '../components/SectionCard';
import { useAuth } from '../context/AuthContext';
import type { Institution } from '../types';

const initialForm = { name: '', cep: '', street: '', number: '', complement: '', district: '', city: '', state: '' };

export function InstitutionsPage() {
  const { token } = useAuth();
  const [rows, setRows] = useState<Institution[]>([]);
  const [form, setForm] = useState(initialForm);
  const [confirmOpen, setConfirmOpen] = useState(false);

  async function loadRows() {
    setRows(await apiRequest<Institution[]>('/institutions', {}, token));
  }

  useEffect(() => { loadRows().catch(console.error); }, []);

  async function createItem() {
    await apiRequest('/institutions', { method: 'POST', body: JSON.stringify(form) }, token);
    setForm(initialForm);
    await loadRows();
    setConfirmOpen(false);
  }

  const columns = useMemo<GridColDef<Institution>[]>(() => [
    { field: 'name', headerName: 'Instituição', flex: 1.1, minWidth: 220 },
    { field: 'cep', headerName: 'CEP', width: 130 },
    { field: 'city', headerName: 'Cidade', width: 180 },
    { field: 'state', headerName: 'Estado', width: 120 },
    { field: 'street', headerName: 'Logradouro', flex: 1, minWidth: 220 },
  ], []);

  return (
    <Stack spacing={3}>
      <SectionCard title="Instituições" action={<Button startIcon={<AddRoundedIcon />} variant="contained" onClick={() => setConfirmOpen(true)}>Salvar instituição</Button>}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}><TextField label="Nome da instituição" fullWidth value={form.name} onChange={(e) => setForm((p) => ({ ...p, name: e.target.value }))} /></Grid>
          <Grid item xs={12} md={3}><TextField label="CEP" fullWidth value={form.cep} onChange={(e) => setForm((p) => ({ ...p, cep: e.target.value }))} /></Grid>
          <Grid item xs={12} md={3}><TextField label="Número" fullWidth value={form.number} onChange={(e) => setForm((p) => ({ ...p, number: e.target.value }))} /></Grid>
          <Grid item xs={12} md={6}><TextField label="Logradouro" fullWidth value={form.street} onChange={(e) => setForm((p) => ({ ...p, street: e.target.value }))} /></Grid>
          <Grid item xs={12} md={6}><TextField label="Complemento" fullWidth value={form.complement} onChange={(e) => setForm((p) => ({ ...p, complement: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Bairro" fullWidth value={form.district} onChange={(e) => setForm((p) => ({ ...p, district: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Cidade" fullWidth value={form.city} onChange={(e) => setForm((p) => ({ ...p, city: e.target.value }))} /></Grid>
          <Grid item xs={12} md={4}><TextField label="Estado" fullWidth value={form.state} onChange={(e) => setForm((p) => ({ ...p, state: e.target.value }))} /></Grid>
        </Grid>
      </SectionCard>
      <SectionCard title="Base cadastrada">
        <Box sx={{ height: 480 }}><DataGrid rows={rows} columns={columns} pageSizeOptions={[10, 20, 50]} /></Box>
      </SectionCard>
      <ConfirmDialog open={confirmOpen} title="Confirmar cadastro" message="Deseja confirmar o cadastro da instituição?" onCancel={() => setConfirmOpen(false)} onConfirm={() => createItem().catch(console.error)} />
    </Stack>
  );
}

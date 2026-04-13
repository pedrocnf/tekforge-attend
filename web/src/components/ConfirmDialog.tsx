import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Typography } from '@mui/material';

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  message: string;
  onCancel: () => void;
  onConfirm: () => void;
}

export function ConfirmDialog({ open, title, message, onCancel, onConfirm }: ConfirmDialogProps) {
  return (
    <Dialog open={open} onClose={onCancel} fullWidth maxWidth="sm">
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <Typography color="text.secondary">{message}</Typography>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 3 }}>
        <Button variant="outlined" onClick={onCancel}>Cancelar</Button>
        <Button variant="contained" onClick={onConfirm}>Confirmar</Button>
      </DialogActions>
    </Dialog>
  );
}

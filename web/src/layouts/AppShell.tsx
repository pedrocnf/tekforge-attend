import DashboardOutlinedIcon from '@mui/icons-material/DashboardOutlined';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import SchoolOutlinedIcon from '@mui/icons-material/SchoolOutlined';
import PersonOutlineOutlinedIcon from '@mui/icons-material/PersonOutlineOutlined';
import PeopleOutlineOutlinedIcon from '@mui/icons-material/PeopleOutlineOutlined';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import LogoutOutlinedIcon from '@mui/icons-material/LogoutOutlined';
import {
  AppBar,
  Box,
  Button,
  Divider,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from '@mui/material';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const drawerWidth = 264;

const menu = [
  { label: 'Dashboard', path: '/app', icon: <DashboardOutlinedIcon /> },
  { label: 'Instituições', path: '/app/institutions', icon: <HomeOutlinedIcon /> },
  { label: 'Disciplinas', path: '/app/disciplines', icon: <SchoolOutlinedIcon /> },
  { label: 'Alunos', path: '/app/students', icon: <PersonOutlineOutlinedIcon /> },
  { label: 'Matrículas', path: '/app/enrollments', icon: <PeopleOutlineOutlinedIcon /> },
  { label: 'Chamadas', path: '/app/attendance', icon: <CalendarMonthOutlinedIcon /> },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="fixed" color="inherit" elevation={0} sx={{ borderBottom: '1px solid', borderColor: 'divider', zIndex: 1300 }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Box>
            <Typography variant="body2" color="text.secondary" sx={{ letterSpacing: 1.6, textTransform: 'uppercase' }}>
              Tekforge ecosystem
            </Typography>
            <Typography variant="h6">Attend</Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box sx={{ textAlign: 'right' }}>
              <Typography variant="body2" fontWeight={700}>{user?.full_name}</Typography>
              <Typography variant="caption" color="text.secondary">{user?.role}</Typography>
            </Box>
            <Button variant="outlined" startIcon={<LogoutOutlinedIcon />} onClick={logout}>Sair</Button>
          </Box>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
            bgcolor: '#0f172a',
            color: '#fff',
            border: 'none',
          },
        }}
      >
        <Toolbar />
        <Box sx={{ px: 3, py: 2 }}>
          <Typography variant="body2" color="rgba(255,255,255,0.7)">Professor · Gestão</Typography>
        </Box>
        <List sx={{ px: 2 }}>
          {menu.map((item) => {
            const selected = location.pathname === item.path;
            return (
              <ListItemButton
                key={item.path}
                component={RouterLink}
                to={item.path}
                selected={selected}
                sx={{
                  borderRadius: 3,
                  mb: 1,
                  color: selected ? '#0f172a' : 'rgba(255,255,255,0.9)',
                  bgcolor: selected ? 'white' : 'transparent',
                  '&:hover': { bgcolor: selected ? 'white' : 'rgba(255,255,255,0.08)' },
                }}
              >
                <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            );
          })}
        </List>
        <Divider sx={{ borderColor: 'rgba(255,255,255,0.1)', mt: 2 }} />
        <Box sx={{ px: 3, py: 2 }}>
          <Typography variant="body2" color="rgba(255,255,255,0.65)">
            www.attend.tekforge.com.br
          </Typography>
          <Typography variant="body2" color="rgba(255,255,255,0.65)">
            api.attend.tekforge.com.br
          </Typography>
        </Box>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1 }}>
        <Toolbar />
        <Box sx={{ p: { xs: 2, md: 3 } }}>{children}</Box>
      </Box>
    </Box>
  );
}

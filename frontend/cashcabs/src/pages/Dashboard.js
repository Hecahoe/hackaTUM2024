import React from 'react';
import { Typography, Box } from '@mui/material';

const Dashboard = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4">Dashboard</Typography>
      <Typography variant="body1">
        Welcome to the dashboard! Add charts, stats, or any relevant information here.
      </Typography>
    </Box>
  );
};

export default Dashboard;

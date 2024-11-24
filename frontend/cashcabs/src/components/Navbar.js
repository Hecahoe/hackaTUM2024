import React from 'react';
import {Link, useLocation} from 'react-router-dom';
import {AppBar, Toolbar, Button, Typography} from '@mui/material';
import "./navbar.css"

const Navbar = () => {

    const location = useLocation(); // Get the current path

    // Function to check if the route is active
    const isActive = (path) => location.pathname === path;

    return (
        <AppBar position="static" sx={{backgroundColor: "white", borderBottom: "4px solid #ea0a8e", color: "black"}}>
            <Toolbar>
                <Typography variant="h6" sx={{flexGrow: 1}}>
                    CashCabs 💸
                </Typography>

                <Button
                    sx={{color: isActive('/') ? '#ea0a8e' : 'black'}}
                    component={Link}
                    to="/"
                >
                    Fleet Manager
                </Button>
                <Button
                    sx={{color: isActive('/dashboard') ? '#ea0a8e' : 'black'}}
                    component={Link}
                    to="/dashboard"
                >
                    Dashboard
                </Button>
            </Toolbar>
        </AppBar>

    );
};

export default Navbar;

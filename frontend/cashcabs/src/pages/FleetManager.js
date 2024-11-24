import React, {useEffect, useState} from 'react';
import MapComponent from "../components/MapComponent";
import {Button, TextField, Box, Typography, IconButton, Collapse} from '@mui/material';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';

const FleetManager = () => {
    const [numCars, setNumCars] = useState(0);
    const [numCustomers, setNumCustomers] = useState(0);
    const [kpiCollapsed, setKpiCollapsed] = useState(false);

    const [scenario, setScenario] = useState(false)
    const [startAnimation, setStartAnimation] = useState(false)

    // State to store fetched data
    const [cars, setCars] = useState([]);
    const [customers, setCustomers] = useState([]);
    const [finishedCustomers, setFinishedCustomers] = useState([]);
    const [routes, setRoutes] = useState([]);

    const handleRunScenario = () => {
        setScenario(true)
        setStartAnimation(false)
        const fetchInitialData = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/initialize");
                const data = await response.json();
                setCars(data.cars);
                setCustomers(data.customers);
                setNumCars(data.cars.length);
                setNumCustomers(data.customers.length);
            } catch (error) {
                console.error("Error fetching initial data:", error);
            }
        };
        fetchInitialData()
    };

    const fetchUpdates = async () => {
        setScenario(false)
        setStartAnimation(true)
        try {
            const response = await fetch("http://127.0.0.1:5000/update");
            const data = await response.json();

            if (data.type === "finished_customers") {
                // Add finished customers to the state
                setFinishedCustomers((prev) => [...prev, ...data.data]);
            } else if (data.type === "new_routes") {
                // Add new routes to the state
                setRoutes((prev) => [...prev, ...data.data]);
            }
        } catch (error) {
            console.error("Error fetching updates:", error);
        }
    };

    useEffect(() => {
        let interval;
        if (startAnimation) {
            interval = setInterval(fetchUpdates, 2000); // Fetch updates every 2 seconds
        } else {
            clearInterval(interval); // Stop fetching updates when animation stops
        }
        return () => clearInterval(interval);
    }, [startAnimation]);

    return (
        <Box
            className="fleet-manager"
            sx={{
                position: 'relative',
                height: '91vh',
                width: '100vw',
                overflow: 'hidden',
            }}
        >
            {/* Map Component (Full-Screen Background) */}
            <Box
                sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    height: '100%',
                    width: '100%',
                    zIndex: 0,
                }}
            >
                <MapComponent
                    startAnimation={startAnimation}
                    cars={cars}
                    customers={customers}
                    finishedCustomers={finishedCustomers}
                    routes={routes}
                />
            </Box>

            {/* Controls Section (Wide Panel) */}
            <Box
                sx={{
                    position: 'absolute',
                    top: '2vh',
                    right: '2vw',
                    width: '90%',
                    height: '6vh',
                    backgroundColor: '#ffffff',
                    padding: 2,
                    borderRadius: 1,
                    zIndex: 1,
                    boxShadow: 4,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                }}
            >
                <TextField
                    label="Number of Cars"
                    type="number"
                    value={numCars}
                    onChange={(e) => setNumCars(e.target.value)}
                    variant="outlined"
                    size="small"
                    sx={{marginRight: 2, width: '20%'}}
                />
                <TextField
                    label="Number of Customers"
                    type="number"
                    value={numCustomers}
                    onChange={(e) => setNumCustomers(e.target.value)}
                    variant="outlined"
                    size="small"
                    sx={{marginRight: 2, width: '20%'}}
                />
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleRunScenario}
                    sx={{height: '100%', width: '15%', backgroundColor: '#ea0a8e'}}
                >
                    Create Scenario
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={fetchUpdates}
                    sx={{height: '100%', width: '15%', backgroundColor: scenario ? "#ea0a8e" : "gray"}}
                >
                    Run Scenario
                </Button>
            </Box>

            {/* KPI Section (Collapsible Red Metrics Area) */}
            <Box
                sx={{
                    position: 'absolute',
                    top: '15vh',
                    right: kpiCollapsed ? '-16vw' : '2vw', // Hide off-screen when collapsed
                    transition: 'right 0.3s ease-in-out', // Smooth transition for collapsing
                    zIndex: 1,
                }}
            >
                <Box
                    sx={{
                        width: '15vw',
                        height: '69vh',
                        backgroundColor: '#ffffff',
                        padding: 1.9,
                        borderRadius: 1,
                        boxShadow: 4,
                        overflow: 'hidden',
                    }}
                >
                    <Typography variant="h6" sx={{marginBottom: 2}}>
                        KPI Metrics
                    </Typography>
                    <Typography variant="body1" sx={{marginBottom: 1}}>
                        <strong>Total Cars:</strong> {numCars}
                    </Typography>
                    <Typography variant="body1" sx={{marginBottom: 1}}>
                        <strong>Total Customers:</strong> {numCustomers}
                    </Typography>
                    <Typography variant="body1">
                        <strong>Scenario Status:</strong> Not Started
                    </Typography>
                </Box>
                {/* Collapse Button */}
                <IconButton
                    onClick={() => setKpiCollapsed(!kpiCollapsed)}
                    sx={{
                        position: 'absolute',
                        top: '50%',
                        left: '-2vh',
                        transform: 'translateY(-50%)',
                        backgroundColor: '#ffffff',
                        boxShadow: 4,
                        borderRadius: '50%',
                        transition: 'background-color 0.3s ease-in-out',
                        '&:hover': {
                            backgroundColor: '#bdbdbd',
                        },
                    }}
                >
                    {kpiCollapsed ? <KeyboardArrowLeftIcon/> : <KeyboardArrowRightIcon/>}
                </IconButton>


            </Box>
        </Box>
    )
        ;
};

export default FleetManager;

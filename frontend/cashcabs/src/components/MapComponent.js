import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import React, { useState } from 'react';
import L from 'leaflet';
import 'leaflet.animatedmarker/src/AnimatedMarker'; // Include the plugin
import startIconImage from '../rsc/startIcon.png';
import EndIconImage from '../rsc/flag.png';
import AnimatedCar from "../components/AnimatedCar";
import CustomerRoutes from "../components/CustomerRoutes";
import "./mapComponent.css";

// Define icons
const carIcon = new L.Icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/744/744465.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15],
});

const startIcon = new L.Icon({
    iconUrl: startIconImage,
    iconSize: [30, 30],
    iconAnchor: [15, 30],
});

const endIcon = new L.Icon({
    iconUrl: EndIconImage,
    iconSize: [30, 30],
    iconAnchor: [15, 25],
});

const MapComponent = ({startAnimation={startAnimation}}) => {
    const center = [48.148966, 11.602188]; // center

    const cars = [
        {
            id: 1,
            startPoint: [48.1351, 11.582],
            endPoint: [48.1451, 11.592],
        },
        {
            id: 2,
            startPoint: [48.19, 11.585],
            endPoint: [48.1500, 11.600],
        },
        {
            id: 3,
            startPoint: [48.1301, 11.580],
            endPoint: [48.1501, 11.595],
        },
    ];

    const customer = [
        {
            id: 4,
            startPoint: [48.14, 11.580],
            endPoint: [48.149, 11.595],
        },
        {
            id: 5,
            startPoint: [48.15, 11.55],
            endPoint: [48.1431, 11.52],
        },
    ];

    return (
        <div className={"map-box"}>
            <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
                <TileLayer
                    url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                    attribution="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://carto.com/'>CARTO</a>"
                />

                {/* Render start and end markers for each customer */}
                {customer.map(customer => (
                    <React.Fragment key={customer.id}>
                        <Marker position={customer.startPoint} icon={startIcon}>
                            <Popup>Start Point</Popup>
                        </Marker>
                        <Marker position={customer.endPoint} icon={endIcon}>
                            <Popup>End Point</Popup>
                        </Marker>
                        <CustomerRoutes
                            key={customer.id}
                            startPoint={customer.startPoint}
                            endPoint={customer.endPoint}
                        />
                    </React.Fragment>
                ))}

                {/* Render animated cars and their routes */}
                {cars.map(car => (
                    <React.Fragment key={car.id}>
                        <Marker position={car.startPoint} icon={startIcon}>
                            <Popup>Start Point</Popup>
                        </Marker>
                        <Marker position={car.endPoint} icon={endIcon}>
                            <Popup>End Point</Popup>
                        </Marker>
                        <AnimatedCar
                            key={car.id}
                            startPoint={car.startPoint}
                            endPoint={car.endPoint}
                            startAnimation={startAnimation}
                        />
                    </React.Fragment>
                ))}
            </MapContainer>
        </div>
    );
};

export default MapComponent;

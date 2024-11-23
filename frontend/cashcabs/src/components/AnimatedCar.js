// src/AnimatedCar.js

import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Polyline, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet.animatedmarker/src/AnimatedMarker';

// Define the car icon
const carIcon = new L.Icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/744/744465.png',
    iconSize: [30, 30],
    iconAnchor: [15, 15],
});

const AnimatedCar = ({ startPoint, endPoint, startAnimation }) => {
    const map = useMap();
    const [testRoute, setTestRoute] = useState([]);

    // Decode polyline function
    const decodePolyline = (encoded) => {
        let index = 0, len = encoded.length, lat = 0, lng = 0;
        const coordinates = [];

        while (index < len) {
            let shift = 0, result = 0;
            let byte;
            do {
                byte = encoded.charCodeAt(index++) - 63;
                result |= (byte & 0x1f) << shift;
                shift += 5;
            } while (byte >= 0x20);
            const dLat = (result & 1) ? ~(result >> 1) : (result >> 1);
            lat += dLat;

            shift = 0;
            result = 0;
            do {
                byte = encoded.charCodeAt(index++) - 63;
                result |= (byte & 0x1f) << shift;
                shift += 5;
            } while (byte >= 0x20);
            const dLng = (result & 1) ? ~(result >> 1) : (result >> 1);
            lng += dLng;

            coordinates.push([lat / 1E5, lng / 1E5]);
        }
        return coordinates;
    };

    // Fetch the route from the API
    const fetchRoute = async (startPoint, endPoint) => {
        const startLngLat = startPoint[1] + "," + startPoint[0];
        const endLngLat = endPoint[1] + "," + endPoint[0];
        const url = `http://router.project-osrm.org/route/v1/driving/${startLngLat};${endLngLat}?overview=full&geometries=polyline`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            const polyline = data.routes[0].geometry;
            const decodedRoute = decodePolyline(polyline);
            setTestRoute(decodedRoute); // Set decoded route into state
        } catch (error) {
            console.error('Error fetching the route:', error);
        }
    };

    // Fetch route when component mounts or startPoint/endPoint change
    useEffect(() => {
        fetchRoute(startPoint, endPoint);
    }, [startPoint, endPoint]);

    // Create animated marker when route is available and animation is triggered
    useEffect(() => {
        if (!startAnimation || testRoute.length === 0) return; // Wait for route and animation trigger

        const animatedMarker = new L.animatedMarker(
            L.polyline(testRoute).getLatLngs(), // Use route coordinates
            {
                icon: carIcon,
                autoStart: true,
                interval: 100, // Interval between frames in ms
            }
        );

        // Add marker to the map
        map.addLayer(animatedMarker);
        animatedMarker.start(); // Start the animation

        // Cleanup on unmount
        return () => {
            map.removeLayer(animatedMarker);
        };
    }, [map, startAnimation, testRoute]); // Re-run effect when animation or route changes

    return (
        <div>
            <Polyline positions={testRoute} color="#EA0A8E" smoothFactor={0}/>
        </div>
    );
};

export default AnimatedCar;

import React, {useEffect, useState} from 'react';
import {Polyline, useMap} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import 'leaflet.animatedmarker/src/AnimatedMarker';
import carIconImage from "../rsc/carIcon.png";
import {popup} from "leaflet/src/layer"; // Import the custom car image

// Define the car icon with dynamic rotation
const carIcon = (rotation) =>
    new L.DivIcon({
        className: 'custom-car-icon',
        html: `<div style="
            transform: rotate(${rotation}deg); 
            width: 30px; 
            height: 30px; 
            background-size: contain; 
            background-repeat: no-repeat; 
            background-image: url('${carIconImage}');
            transition: transform 1s ease-in-out;
        ">
</div>`,
        iconAnchor: [6, 15],

    });

const AnimatedCar = ({startPoint, endPoint, startAnimation}) => {
    const map = useMap();

    const [testRoute, setTestRoute] = useState([]);
    const [currentAngle, setCurrentAngle] = useState(0);

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

            coordinates.push([lat / 1e5, lng / 1e5]);
        }
        return coordinates;
    };

    // Interpolate points to make them evenly spaced
    const interpolateRoute = (route, distance = 10) => {
        const toRadians = (degrees) => (degrees * Math.PI) / 180;

        const interpolate = (pointA, pointB, t) => [
            pointA[0] + (pointB[0] - pointA[0]) * t,
            pointA[1] + (pointB[1] - pointA[1]) * t,
        ];

        const calculateDistance = ([lat1, lng1], [lat2, lng2]) => {
            const R = 6371000; // Earth radius in meters
            const dLat = toRadians(lat2 - lat1);
            const dLng = toRadians(lng2 - lng1);
            const a =
                Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(toRadians(lat1)) *
                Math.cos(toRadians(lat2)) *
                Math.sin(dLng / 2) *
                Math.sin(dLng / 2);
            return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        };

        const interpolated = [];
        for (let i = 0; i < route.length - 1; i++) {
            const [start, end] = [route[i], route[i + 1]];
            const segmentDistance = calculateDistance(start, end);
            const segmentSteps = Math.ceil(segmentDistance / distance);
            for (let step = 0; step < segmentSteps; step++) {
                interpolated.push(interpolate(start, end, step / segmentSteps));
            }
        }
        interpolated.push(route[route.length - 1]); // Add the last point
        return interpolated;
    };

    // Calculate the bearing between two points
    const calculateBearing = ([lat1, lon1], [lat2, lon2]) => {
        const toRadians = (degrees) => (degrees * Math.PI) / 180;
        const toDegrees = (radians) => (radians * 180) / Math.PI;

        const dLon = toRadians(lon2 - lon1);
        const y = Math.sin(dLon) * Math.cos(toRadians(lat2));
        const x =
            Math.cos(toRadians(lat1)) * Math.sin(toRadians(lat2)) -
            Math.sin(toRadians(lat1)) *
            Math.cos(toRadians(lat2)) *
            Math.cos(dLon);
        return (toDegrees(Math.atan2(y, x)) + 360) % 360; // Bearing in degrees
    };

    // Fetch the route from the API
    const fetchRoute = async (startPoint, endPoint) => {
        const startLngLat = startPoint[1] + ',' + startPoint[0];
        const endLngLat = endPoint[1] + ',' + endPoint[0];
        const url = `http://router.project-osrm.org/route/v1/driving/${startLngLat};${endLngLat}?overview=full&geometries=polyline`;

        try {
            const response = await fetch(url);
            const data = await response.json();
            const polyline = data.routes[0].geometry;
            const decodedRoute = decodePolyline(polyline);
            const smoothedRoute = interpolateRoute(decodedRoute, 5); // Interpolate with a 10-meter step
            setTestRoute(smoothedRoute); // Set the smoothed route into state
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

        const latLngs = L.polyline(testRoute).getLatLngs();

        const animatedMarker = new L.Marker(latLngs[0], {
            icon: carIcon(currentAngle), // Initial rotation
        });

        map.addLayer(animatedMarker);

        let currentIndex = 0;
        const interval = setInterval(() => {
            if (currentIndex < latLngs.length - 1) {
                const nextIndex = currentIndex + 1;
                const angle = calculateBearing(
                    [latLngs[currentIndex].lat, latLngs[currentIndex].lng],
                    [latLngs[nextIndex].lat, latLngs[nextIndex].lng]
                );
                setCurrentAngle(angle); // Update rotation
                animatedMarker.setIcon(carIcon(angle));
                animatedMarker.setLatLng(latLngs[nextIndex]);
                currentIndex = nextIndex;
            } else {
                clearInterval(interval); // Stop animation at the end
            }
        }, 40); // Adjust interval for smooth movement

        return () => {
            map.removeLayer(animatedMarker);
            clearInterval(interval); // Cleanup on unmount
        };
    }, [startAnimation]); // Re-run effect when animation or route changes

    return (
        <div>
            <Polyline positions={testRoute} color="#EA0A8E" smoothFactor={0}/>
        </div>
    );
};

export default AnimatedCar;

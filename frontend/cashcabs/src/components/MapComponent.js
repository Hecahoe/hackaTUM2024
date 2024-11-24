import {MapContainer, TileLayer, Marker, Popup, useMap} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import React, {useState} from 'react';
import L from 'leaflet';
import 'leaflet.animatedmarker/src/AnimatedMarker'; // Include the plugin
import startIconImage from '../rsc/startIcon.png';
import EndIconImage from '../rsc/flag.png';
import AnimatedCar from "../components/AnimatedCar";
import CustomerRoutes from "../components/CustomerRoutes";
import "./mapComponent.css";
import carIconImage from "../rsc/carIcon.png";


// Define icons
const carIcon = new L.Icon({
    iconUrl: carIconImage, iconSize: [12, 30], iconAnchor: [6, 15],
});

const startIcon = new L.Icon({
    iconUrl: startIconImage, iconSize: [30, 30], iconAnchor: [0, 0],
});

const endIcon = new L.Icon({
    iconUrl: EndIconImage, iconSize: [30, 30], iconAnchor: [15, 25],
});

const MapComponent = ({
                          startAnimation = {startAnimation},
                          cars = {cars},
                          customers = {customers},
                          finishedCustomers = {finishedCustomers},
                          routes = {routes}
                      }) => {
    const center = [48.148966, 11.602188]; // center



    return (<div className={"map-box"}>
        <MapContainer center={center} zoom={13} style={{height: '100%', width: '100%'}}>
            <TileLayer
                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
            />

            {/* Render start and end markers for each customer */}
            {cars.map(car => {
                if (car.position) {
                    return ((<React.Fragment key={car.id}>
                            <Marker position={car.position} icon={carIcon}>
                                <Popup>Inactive Car: {car.id}</Popup>
                            </Marker>
                        </React.Fragment>

                    ))
                }
            })}
            {finishedCustomers.map(customer => {
                if (customer.position) {
                    return (
                        (<React.Fragment key={customer.id}>
                                <Marker position={customer.position} icon={carIcon}>
                                    <Popup>Finished Customer: {customer.id}</Popup>
                                </Marker>
                            </React.Fragment>

                        )
                    )
                }

            })}
            {customers.map(customer => {

                    if (customer?.start && customer?.end) {
                        return (<React.Fragment key={customer.id}>
                            <Marker position={customer.start} icon={startIcon}>
                                <Popup>Start Point: {customer.id}</Popup>
                            </Marker>
                            <Marker position={customer.end} icon={endIcon}>
                                <Popup>End Point: {customer.id}</Popup>
                            </Marker>
                            <CustomerRoutes
                                key={customer.id}
                                startPoint={customer.start}
                                endPoint={customer.end}
                            />
                        </React.Fragment>)
                    }
                }
            )
            }

            {/* Render animated cars and their routes */}
            {routes.map((route, index) => {


                if (route?.start && route?.end) {
                    return (<React.Fragment key={`route-${route.car_id}`}>
                        <AnimatedCar
                            key={`animated-car-${index}`} // Ensure unique key
                            startPoint={route.start}
                            endPoint={route.end}
                            time={route.time}
                            startAnimation={true}
                        />
                    </React.Fragment>)
                }


            })}

        </MapContainer>
    </div>)
        ;
};

export default MapComponent;

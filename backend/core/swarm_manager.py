# backend/core/swarm_manager.py

import threading
import time
import random
from typing import Dict

from backend.hardware.abstract_drone import AbstractDrone
from backend.hardware.drone_simulator import DroneSimulator
from backend.hardware.tello_drone import TelloDrone
from backend import config

class SwarmManager:
    DRONE_DRIVERS = {
        'SIMULATOR': DroneSimulator,
        'TELLO': TelloDrone,
    }

    def __init__(self):
        self.drones: Dict[str, AbstractDrone] = {}
        self.base_location = config.BASE_LOCATION
        self.initialize_swarm()

    def initialize_swarm(self):
        DroneClass = self.DRONE_DRIVERS.get(config.DRONE_TYPE)
        if not DroneClass:
            raise ValueError(f"Tipo de drone desconhecido: {config.DRONE_TYPE}")

        for i in range(config.NUM_DRONES):
            drone_id = f"Drone-{i+1}"
            
            kwargs = {}
            if config.DRONE_TYPE == 'SIMULATOR':
                offset_lat = (random.random() - 0.5) * 0.002
                offset_lon = (random.random() - 0.5) * 0.002
                kwargs['start_pos'] = [self.base_location[0] + offset_lat, self.base_location[1] + offset_lon, 20.0]
            elif config.DRONE_TYPE == 'TELLO':
                kwargs['ip_address'] = config.TELLO_IPS[i]

            drone = DroneClass(drone_id=drone_id, **kwargs)
            if drone.connect():
                self.drones[drone_id] = drone

    def get_swarm_telemetry(self):
        return [drone.get_telemetry().dict() for drone in self.drones.values()]

    def command_go_to_all(self, target_pos, speed=5):
        """Envia um comando 'go_to' para todos os drones não offline."""
        print(f"Enviando enxame para coordenadas: {target_pos}")
        for drone in self.drones.values():
            telemetry = drone.get_telemetry()
            if telemetry.status not in ["Offline", "Landed", "Disconnected"]:
                # O comando go_to espera lat, lon, alt, speed
                drone.go_to(target_pos[0], target_pos[1], target_pos[2], speed)

    def command_takeoff_all(self):
        for drone in self.drones.values():
            drone.takeoff()

    def command_land_all(self):
        for drone in self.drones.values():
            drone.land()
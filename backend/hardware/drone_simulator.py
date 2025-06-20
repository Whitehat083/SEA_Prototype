import threading
import time
import math
import random
from backend.hardware.abstract_drone import AbstractDrone
from backend.core.telemetry import TelemetryData
from backend.config import SIM_MAX_SPEED, SIM_BATTERY_DRAIN_IDLE, SIM_BATTERY_DRAIN_MOVING

class DroneSimulator(AbstractDrone, threading.Thread):
    def __init__(self, drone_id: str, start_pos: list, **kwargs):
        AbstractDrone.__init__(self, drone_id)
        threading.Thread.__init__(self, daemon=True)
        
        self.telemetry = TelemetryData(
            drone_id=drone_id,
            status="Landed",
            position=start_pos,
            battery=100
        )
        self.target = start_pos
        self.lock = threading.Lock()
        self.running = True

    def connect(self) -> bool:
        with self.lock:
            if self.telemetry.status == "Offline":
                self.telemetry.status = "Landed"
        self.start()
        return True

    def disconnect(self):
        self.running = False
        with self.lock:
            self.telemetry.status = "Offline"
    
    def takeoff(self):
        with self.lock:
            if self.telemetry.status == "Landed":
                self.telemetry.status = "TakingOff"
        time.sleep(2)
        with self.lock:
            if self.telemetry.status == "TakingOff":
                self.telemetry.status = "Idle"
    
    def land(self):
        with self.lock:
            self.telemetry.status = "Landing"
        time.sleep(3)
        with self.lock:
            if self.telemetry.status == "Landing":
                self.telemetry.status = "Landed"

    def go_to(self, lat, lon, alt, speed):
        with self.lock:
            self.target = [lat, lon, alt]
            self.telemetry.status = "Moving"
            
    def hold_position(self):
        with self.lock:
            if self.telemetry.status not in ["Landed", "Offline"]:
                self.telemetry.status = "Idle"
                self.target = self.telemetry.position

    def get_telemetry(self) -> TelemetryData:
        with self.lock:
            return self.telemetry.copy()
            
    def run(self):
        while self.running:
            with self.lock:
                if self.telemetry.status in ["Moving", "Returning"]:
                    self._move()
                self._drain_battery()
            time.sleep(1)

    def _move(self):
        pos = self.telemetry.position
        dist_lat = self.target[0] - pos[0]
        dist_lon = self.target[1] - pos[1]
        distance = math.sqrt(dist_lat**2 + dist_lon**2)

        if distance < 0.0001:
            if self.telemetry.status == "Moving":
                self.telemetry.status = "Idle"
            return
            
        dir_lat = dist_lat / distance
        dir_lon = dist_lon / distance
        pos[0] += dir_lat * SIM_MAX_SPEED
        pos[1] += dir_lon * SIM_MAX_SPEED
    
    def _drain_battery(self):
        if self.telemetry.battery and self.telemetry.battery > 0:
            drain = SIM_BATTERY_DRAIN_MOVING if self.telemetry.status in ["Moving", "Returning"] else SIM_BATTERY_DRAIN_IDLE
            self.telemetry.battery -= drain
        if self.telemetry.battery is not None and self.telemetry.battery <= 0:
            self.telemetry.battery = 0
            self.telemetry.status = "Offline"
            self.running = False

from backend.hardware.abstract_drone import AbstractDrone
from backend.core.telemetry import TelemetryData
from djitellopy import Tello

class TelloDrone(AbstractDrone):
    def __init__(self, drone_id: str, ip_address: str, **kwargs):
        super().__init__(drone_id)
        self.ip = ip_address
        self.tello = Tello(host=self.ip)
        self.telemetry = TelemetryData(drone_id=drone_id, status="Offline")

    def connect(self) -> bool:
        print(f"[{self.drone_id}] Trying to connect to {self.ip}...")
        try:
            self.tello.connect()
            self.telemetry.status = "Landed"
            print(f"[{self.drone_id}] Connection successful.")
            return True
        except Exception as e:
            print(f"[{self.drone_id}] Connection failed: {e}")
            return False

    def disconnect(self):
        self.tello.end()
        self.telemetry.status = "Offline"

    def takeoff(self):
        print(f"[{self.drone_id}] Takeoff command sent.")
        self.tello.takeoff()
        self.telemetry.status = "TakingOff"

    def land(self):
        self.tello.land()
        self.telemetry.status = "Landing"

    def go_to(self, lat: float, lon: float, alt: float, speed: int):
        print(f"[{self.drone_id}] GO_TO COMMAND IS NOT IMPLEMENTED FOR TELLO (No GPS).")
        self.telemetry.status = "Idle"

    def hold_position(self):
        self.tello.stop()
        self.telemetry.status = "Idle"

    def get_telemetry(self) -> TelemetryData:
        try:
            self.telemetry.battery = self.tello.get_battery()
            if self.tello.is_flying and self.telemetry.status not in ["Moving", "Returning", "Landing", "TakingOff"]:
                self.telemetry.status = "Idle"
            elif not self.tello.is_flying and self.telemetry.status not in ["Offline", "Disconnected"]:
                self.telemetry.status = "Landed"
            return self.telemetry.copy()
        except Exception:
            self.telemetry.status = "Offline"
            return self.telemetry.copy()

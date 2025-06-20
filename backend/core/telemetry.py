from pydantic import BaseModel
from typing import List, Optional, Literal

DroneStatus = Literal[
    "Offline", "Disconnected", "Landed", "Idle", "TakingOff",
    "Returning", "Moving", "Holding", "Landing"
]

class TelemetryData(BaseModel):
    drone_id: str
    status: DroneStatus = "Offline"
    position: Optional[List[float]] = None  # [lat, lon, alt]
    battery: Optional[int] = None           # 0-100
    heading: Optional[int] = None           # 0-359
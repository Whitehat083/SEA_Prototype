import sys
import os
import time
import random

# -- Project Root Setup --
# Adds the project's root directory to the Python path.
# This allows for absolute imports from the 'backend' package.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(PROJECT_ROOT)

from backend.core.swarm_manager import SwarmManager
from backend.config import BASE_LOCATION

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_telemetry(swarm: SwarmManager):
    telemetry_data = swarm.get_swarm_telemetry()
    
    print("================== [ SEA SWARM TELEMETRY ] ==================")
    for data in telemetry_data:
        drone_id = data.get('drone_id', 'N/A')
        status = data.get('status', 'N/A')
        battery = data.get('battery', 'N/A')
        if data.get('position'):
            lat, lon, alt = data['position']
            pos_str = f"Pos: ({lat:.4f}, {lon:.4f}) @ {alt:.1f}m"
        else:
            pos_str = "Pos: N/A"

        print(f"  > ID: {drone_id:<10} | Status: {status:<12} | Battery: {battery:>3}% | {pos_str}")
    print("================================================================")
    print("(Press Ctrl+C to skip to the next step)")

def run_test():
    clear_screen()
    print(">>> INITIALIZING SWARM MANAGER TEST SCRIPT <<<")
    print(">>> Ensure 'DRONE_TYPE' in config.py is set to 'SIMULATOR'.\n")

    print("--> [1] Initializing SwarmManager...")
    swarm = SwarmManager()
    print(f"--> SwarmManager initialized with {len(swarm.drones)} virtual drones.")
    time.sleep(2)
    
    print("\n--> [2] Observing initial state (5 seconds)...")
    try:
        end_time = time.time() + 5
        while time.time() < end_time:
            clear_screen()
            print("--> [2] Observing initial state (drones should be 'Landed')...")
            print_telemetry(swarm)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    print("\n--> [3] Sending global TAKEOFF command...")
    swarm.command_takeoff_all()
    print("--> Observing takeoff sequence (8 seconds)...")
    try:
        end_time = time.time() + 8
        while time.time() < end_time:
            clear_screen()
            print("--> [3] Drones are now taking off and changing to 'Idle' (hovering)...")
            print_telemetry(swarm)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        
    random_lat_offset = (random.random() - 0.5) * 0.02
    random_lon_offset = (random.random() - 0.5) * 0.02
    target_position = [
        BASE_LOCATION[0] + random_lat_offset,
        BASE_LOCATION[1] + random_lon_offset,
        50.0
    ]
    
    print(f"\n--> [4] Sending global GO_TO command to a random target...")
    swarm.command_go_to_all(target_position)
    print("--> Observing movement (15 seconds)...")
    try:
        end_time = time.time() + 15
        while time.time() < end_time:
            clear_screen()
            print("--> [4] Drones are in motion (status 'Moving')...")
            print_telemetry(swarm)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    print("\n--> [5] Sending global LAND command...")
    swarm.command_land_all()
    print("--> Observing landing sequence (8 seconds)...")
    try:
        end_time = time.time() + 8
        while time.time() < end_time:
            clear_screen()
            print("--> [5] Drones are landing (status 'Landing')...")
            print_telemetry(swarm)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    print("\n>>> TEST COMPLETE! <<<")
    clear_screen()
    print(">>> Final drone state:")
    print_telemetry(swarm)

if __name__ == "__main__":
    run_test()

# -- CONFIGURAÇÕES GERAIS --
# Mude 'SIMULATOR' para 'TELLO' para usar drones Tello reais (quando implementado)
DRONE_TYPE = 'SIMULATOR'

BASE_LOCATION = [40.7128, -74.0060]  # Localização padrão da base
NUM_DRONES = 8 if DRONE_TYPE == 'SIMULATOR' else 4  # Número de drones a serem inicializados

# -- CONFIGURAÇÕES DO SIMULADOR (se DRONE_TYPE for 'SIMULATOR') --
SIM_MAX_SPEED = 0.0003
SIM_COMMS_RANGE = 0.05
SIM_BATTERY_DRAIN_MOVING = 0.08
SIM_BATTERY_DRAIN_IDLE = 0.01

# -- CONFIGURAÇÕES DO DRONE TELLO (se DRONE_TYPE for 'TELLO') --
# Os endereços IP dos seus drones Tello. O sistema se conectará a estes.
# O Tello, por padrão, cria sua própria rede Wi-Fi. Você precisará se conectar a cada
# um para configurá-los para se juntarem à sua rede Wi-Fi central (modo estação).
TELLO_IPS = [
    "192.168.1.101",
    "192.168.1.102",
    "192.168.1.103",
    "192.168.1.104",
]


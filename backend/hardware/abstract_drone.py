from abc import ABC, abstractmethod
from backend.core.telemetry import TelemetryData

class AbstractDrone(ABC):
    """
    Define a interface que todo driver de drone (real ou simulado) deve implementar.
    O SwarmManager interagirá com qualquer drone através destes métodos.
    """

    @abstractmethod
    def __init__(self, drone_id: str, **kwargs):
        """Inicializa o drone com sua ID e configurações específicas."""
        self.drone_id = drone_id

    @abstractmethod
    def connect(self) -> bool:
        """Estabelece a conexão com o drone. Retorna True se for bem-sucedido."""
        pass

    @abstractmethod
    def disconnect(self):
        """Encerra a conexão com o drone."""
        pass

    @abstractmethod
    def takeoff(self):
        """Comanda o drone para decolar."""
        pass

    @abstractmethod
    def land(self):
        """Comanda o drone para pousar."""
        pass

    @abstractmethod
    def go_to(self, lat: float, lon: float, alt: float, speed: int):
        """Comanda o drone para se mover para uma coordenada GPS."""
        pass

    @abstractmethod
    def hold_position(self):
        """Comanda o drone para parar e manter a posição atual."""
        pass

    @abstractmethod
    def get_telemetry(self) -> TelemetryData:
        """Retorna os dados de telemetria atuais do drone."""
        pass

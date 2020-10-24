from modules.settings import EventType
from modules.connection import *     

class Event:
    def __init__(self, parent, *args, **kwargs):
        
        self.parent = parent

    def setRequestEvent(self, time: float) -> None:
        """Configura os eventos e a conexão

        Args:
            time (float): Tempo de evento
        """
        self.time = time
        self.type_req = EventType.Req
        self.setNextEvent(None)
        self.setConnection(None)
    
    def setNextEvent(self, event) -> None:
        """Configura o próximo evento

        Args:
            event (Event): Próximo evento
        """
        self.next_event = event

    def getNextEvent(self):
        """Retorna o próximo evento

        Returns:
            Event: Próximo evento
        """
        return self.next_event

    def setConnection(self, connection: Connection) -> None:
        """Configura a conexão

        Args:
            connection (Connection): Conexão
        """
        self.connection = connection

    def getTime(self) -> float:
        """Retorna o tempo do evento

        Returns:
            float: Tempo do evento atual
        """
        return self.time
    
    def getType(self) -> EventType:
        return self.type_req
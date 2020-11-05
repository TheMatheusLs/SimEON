from modules.settings import *      # Modulo com as configurações e as constantes usadas ao logo do código


class Definitions:
    def __init__(self, parent, *args, **kwargs) -> None:

        self.parent = parent
        
        print(f"\n* Routing:\n"  + ''.join([f" {value.value} <-- {key}\n" for key, value in RoutingCode.__members__.items()]))
        #self.routing_algorithm = int(input("Insert Desired Routing Algorithm: "))
        self.routing_algorithm = RoutingCode.Dijkstra.value
        self.routing_algorithm_name = [key for key, value in RoutingCode.__members__.items() if self.routing_algorithm == value.value][0]

        assert(self.routing_algorithm in [value.value for _, value in RoutingCode.__members__.items()])

        print(f"* Spectrum Assignment:\n" + ''.join([f" {value.value} <-- {key.replace('_', ' with tiebreaker by ')}\n" for key, value in SpectrumCode.__members__.items()]))
        self.alocation_algorithm = int(input("Insert Desired Spectrum Assignment: "))
        #self.alocation_algorithm = 0
        self.alocation_algorithm_name = [key for key, value in SpectrumCode.__members__.items() if self.alocation_algorithm == value.value][0]

        assert(self.alocation_algorithm in [value.value for _, value in SpectrumCode.__members__.items()])

        print(f"*Traffic Parameters:")
        #self.mu = int(input("Insert Connection Deactivation Rate: (Default: 1): "))
        self.mu = 1
        #self.LaNetMin = int(input("LaNet Min = "))
        self.LaNetMin = 20
        #self.LaNetMax = int(input("LaNet Max = "))
        self.LaNetMax = 100
        #self.Npontos = int(input("#Points in the Graph = "))
        self.Npontos = 5
        #self.LaPasso = (self.LaNetMax - self.LaNetMin) // (self.Npontos - 1)

        #self.numReq = int(input("Insert Number of Requests: (Recommended: > 1000000): "))
        self.numReq = 1_000_000

        self.setNumReqMax(self.numReq)

        #self.slotBW = 12_500_000_000
        self.slotBW = 400_000_000_000

    def initialise(self) -> None:
        """Inicializa as váriaveis
        """
        self.numReq = 0.0
        self.numReq_Bloq = 0.0
        self.numSlots_Req = 0.0
        self.numSlots_Bloq = 0.0
        self.numHopsPerRoute = 0.0
        self.netOccupancy = 0.0
    
    def getNumReq(self) -> int:
        """Retorna o número de requisições

        Returns:
            int: Número de requisições
        """
        return self.numReq

    def getNumReqMax(self) -> int:
        """Retorna o número máximo de requisições

        Returns:
            int: Número máximo de requisições
        """
        return self.numReqMax

    def setNumReqMax(self, numReqMax: int) -> None:
        """Configura o número máximo de requisições

        Args:
            numReqMax (int): Número máximo 
        """
        self.numReqMax = numReqMax


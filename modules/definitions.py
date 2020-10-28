from modules.settings import *      # Modulo com as configurações e as constantes usadas ao logo do código


class Definitions:
    def __init__(self, parent, *args, **kwargs) -> None:

        self.parent = parent
        
        print(f"* Routing:  {DJK_code} - DJK     {YEN_code} - YEN")
        #self.routing_algorithm = int(input("Insert Desired Routing Algorithm: "))
        self.routing_algorithm = 0

        print(f"* Spectrum Assignment:  {RD_code} - Random {FF_code} - FirstFit")
        #self.alocation_algorithm = int(input("Insert Desired Spectrum Assignment: "))
        self.alocation_algorithm = 0

        print(f"*Traffic Parameters:")
        #self.mu = int(input("Insert Connection Deactivation Rate: (Default: 1): "))
        self.mu = 1
        #self.LaNetMin = int(input("LaNet Min = "))
        self.LaNetMin = 1
        #self.LaNetMax = int(input("LaNet Max = "))
        self.LaNetMax = 5
        #self.Npontos = int(input("#Points in the Graph = "))
        self.Npontos = 2
        self.LaPasso = (self.LaNetMax - self.LaNetMin) // (self.Npontos - 1)

        #self.nReq = int(input("Insert Number of Requests: "))
        self.numReq = 100_000

        self.setNumReqMax(self.numReq)

        self.slotBW = 12500000000

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


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
        self.LaNetMin = 20
        #self.LaNetMax = int(input("LaNet Max = "))
        self.LaNetMax = 100
        #self.Npontos = int(input("#Points in the Graph = "))
        self.Npontos = 5
        self.LaPasso = (self.LaNetMax - self.LaNetMin) / (self.Npontos - 1)

        #self.nReq = int(input("Insert Number of Requests: "))
        self.nReq = 5

    def initialise(self):
        self.numReq = 0.0
        self.numReq_Bloq = 0.0
        self.numSlots_Req = 0.0
        self.numSlots_Bloq = 0.0
        self.numHopsPerRoute = 0.0
        self.netOccupancy = 0.0

import json                         # Importa o modulo para trabalhar com arquivos .json
import math
from modules.settings import *      # Modulo com as configurações e as constantes usadas ao logo do código
from modules.topology import *      # Modulo para armazenar e manipular a topologia da rede
from modules.traffic import *       # Modulo para armazenar e manipular a tráfego da rede
from modules.definitions import *   # Modulo para armazenar e manipular as definições
from modules.schedule import *      # Modulo para controlar a execução do tempo
from modules.routing import *       # Modulo para controlar o roteamento   
from modules.event import *         # Modulo para controlar os eventos
from modules.assignment import *    # Modulo para
import modules.modulation as Modulation
import modules.heuristics as Heuristic
class Main:
    def __init__(self, *args, **kwargs) -> None:

        # Cria os objetos para cada classe
        self.topology = Topology(TOPOLOGY_PATH, self)
        self.traffic = Traffic(TRAFFIC_PATH, self)
        self.definitions = Definitions(self)
        self.schedule = Schedule(self)

        # Inicializa todas as classes
        self.topology.initialise()
        self.definitions.initialise()
        self.schedule.initialise()

        # Encontra as todas as rotas usando o algoritmo escolhido
        self.routing = Routing(self.definitions.routing_algorithm, self)

        # Escreve todas as rotas na tela
        self.topology.printAllRoutes()

        print("Start Of Simulation: \n")

        for laNet in range(self.definitions.LaNetMin, self.definitions.LaNetMax + 1, self.definitions.LaPasso):
            self.simulate(laNet)

    def simulate(self, laNet: float) -> None:
        print("Network Topology")

        # Inicializa todas as classes
        self.topology.initialise()
        self.definitions.initialise()
        self.schedule.initialise()

        # Cria o evento para ser a primeira requisição
        event = Event(self)
        event.setRequestEvent(self.schedule.getSimTime())
        self.schedule.scheduleEvent(event)

        while (self.definitions.getNumReq() < self.definitions.getNumReqMax()):

            curEvent = self.schedule.getCurrentEvent()

            if (curEvent.getType() == EventType.Req): # Chegou uma requisição
                print(f"NumReq = {self.definitions.numReq}") # Colocar o par de origem e destino
                self.ConnectionRequest(curEvent)

    def ConnectionRequest(self, event: Event) -> None:
        self.definitions.numReq += 1

        origin_node, destination_node = self.traffic.sourceDestinationTrafficRequest()

        assert(self.topology.valid_node(origin_node) and self.topology.valid_node(destination_node))

        bps = self.traffic.bitRateTrafficRequest()

        ber = self.traffic.getBER()

        polarization = self.traffic.getPolarization()

        assignment = Assignment(origin_node, destination_node, self)

        M = 4

        #Do
        assignment.setNumSlots(math.ceil(Modulation.bandwidthQAM(M, bps, polarization) / self.definitions.slotBW))
        assignment.setOSNRth(Modulation.getSNRbQAM(M, ber))

        #TODO: Continuar
        #Roteamento:
        #Heuristics.Routing(assignment, self)

        


        

if __name__ == "__main__":
    
    Main()

    print("Finish Simulation: ")
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
from modules.heuristics import *
from modules.connection import *
import modules.general as General

class Main:
    def __init__(self, *args, **kwargs) -> None:

        # Cria os objetos para cada classe
        self.topology = Topology(TOPOLOGY_PATH, self)
        self.traffic = Traffic(TRAFFIC_PATH, self)
        self.definitions = Definitions(self)
        self.schedule = Schedule(self)
        self.heuristics = Heuristic(self)

        # Inicializa todas as classes
        self.topology.initialise()
        self.definitions.initialise()
        self.schedule.initialise()

        # Encontra as todas as rotas usando o algoritmo escolhido
        self.routing = Routing(self)

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
        self.schedule.initialise() # Essa linha não está no arquivo c++

        # Cria o evento para ser a primeira requisição
        event = Event(self)
        event.setRequestEvent(self.schedule.getSimTime())
        self.schedule.scheduleEvent(event)

        while (self.definitions.getNumReq() < self.definitions.getNumReqMax()):

            curEvent = self.schedule.getCurrentEvent()

            if (curEvent.getType() == EventType.Req): # Chegou uma requisição
                print(f"NumReq = {self.definitions.numReq}") # Colocar o par de origem e destino
                self.ConnectionRequest(curEvent)

                IAT = General.exponential(laNet) #Inter-arrival time

                curEvent.setRequestEvent(curEvent, self.schedule.getSimTime() + IAT) #Reuse the same Event Object
                assert(event.getType() == EventType.Req)
                assert(event.getConnection() == None)
                self.schedule.scheduleEvent(curEvent)
            else:
                if curEvent.getType() == EventType.Desc: #Desconnection Request
                    self.ConnectionRelease(curEvent)
                    del curEvent
                else:
                    if (curEvent.getType() == EventType.Exp):
                        #assert(ExpComp) #Um evento deste tipo so pode ocorrer se ExpComp=true;
                        self.heuristics.ExpandConnection(curEvent.getConnection())
                        #DefineNextEventOfCon(curEvent)
                        self.schedule.scheduleEvent(curEvent)
                    else:
                        if (curEvent.getType() == EventType.Comp):
                            #assert(ExpComp) #Um evento deste tipo so pode ocorrer se ExpComp=true;
                            self.heuristics.CompressConnection(curEvent.getConnection())
                            #DefineNextEventOfCon(curEvent)
                            self.schedule.scheduleEvent(curEvent)
        self.FinaliseAll(laNet)



    #TODO: Mudar o bloqueio para 1 a 5 erlangs


    def FinaliseAll(self, laNet) -> None:
        print(f"Simulation Time= {self.schedule.getSimTime()}  numReq= {self.definitions.numReq}")
        print(f"nu0= {laNet}  PbReq= {self.definitions.numReq_Bloq / self.definitions.numReq} PbSlots = {self.definitions.numSlots_Bloq / self.definitions.numSlots_Req} HopsMed = {self.definitions.numHopsPerRoute / (self.definitions.numReq - self.definitions.numReq_Bloq) } netOcc = {self.definitions.netOccupancy}")

        with open(".\\others\\result.txt", 'r') as result_file:
            result_file.write(f"{laNet} {self.definitions.numReq_Bloq / self.definitions.numReq} {self.definitions.numSlots_Bloq / self.definitions.numSlots_Req} {self.definitions.numHopsPerRoute / (self.definitions.numReq - self.definitions.numReq_Bloq) } {self.definitions.netOccupancy}")

        evtPtr = self.schedule.getCurrentEvent()

        while (evtPtr != None):
            con = evtPtr.getConnection()
            if con != None: # This is a Connection
                self.topology.releaseConnection(con)
                del con
            del evtPtr
            evtPtr = self.schedule.getCurrentEvent()

        assert(not self.topology.areThereOccupiedSlots())
        assert(self.schedule.isEmpty())


    def ConnectionRelease(self, evt) -> None:
        connection = evt.getConnection()
        self.topology.releaseConnection(connection)
        del connection

    def ConnectionRequest(self, event: Event) -> None:
        self.definitions.numReq += 1

        origin_node, destination_node = self.traffic.sourceDestinationTrafficRequest()

        assert(self.topology.valid_node(origin_node) and self.topology.valid_node(destination_node))

        bps = self.traffic.bitRateTrafficRequest()

        ber = self.traffic.getBER()

        polarization = self.traffic.getPolarization()

        assignment = Assignment(origin_node, destination_node, self)

        M = 4

        DO = True
        while ((M>1) or (DO)):
            DO = False
            assignment.setNumSlots(math.ceil(Modulation.bandwidthQAM(M, bps, polarization) / self.definitions.slotBW))
            assignment.setOSNRth(Modulation.getSNRbQAM(M, ber))

            #Roteamento:
            self.heuristics.Routing(assignment)

            if ( (assignment.getRoute() != None) and ( self.topology.valid_node(assignment.getOrN())) and (self.topology.valid_node(assignment.getDeN()))): 
                self.heuristics.FirstFit(assignment)

                if ( (assignment.getSlot_inic() != -1) and (assignment.getSlot_fin() != -1)):
                    # Request was accepted
                    
                    newConnection = Connection(assignment.getRoute(), assignment.getSlot_inic(), assignment.getSlot_fin(), self.schedule.getSimTime() + General.exponential(self.definitions.mu))

                    self.topology.connect(newConnection)

                    evtNewCon = Event(self)
                    evtNewCon.setReleaseEvent(evtNewCon, newConnection)

                    self.schedule.scheduleEvent(evtNewCon)

                    break

            M -= 1   

        if M == 1:
            self.definitions.numReq_Bloq += 1      
        
        del assignment



if __name__ == "__main__":
    
    Main()

    print("Finish Simulation: ")

import random
from random import sample
from modules.settings import RAND_MAX, FF_code, RD_code, SLOT_FREE
from modules.assignment import Assignment

import logging

LOG_FORMAT = "%(asctime)s | %(levelname)s - %(message)s" 
logging.basicConfig(filename = "simulation.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = 'a')
logger = logging.getLogger()

class Heuristic:
    def __init__(self, parent, *args, **kwargs) -> None:

        self.parent = parent

    def Routing(self, assignment):
        #routeSet = self.parent.routing.Dijkstra(assignment.getOrN(), assignment.getDeN())

        #self.parent.topology.set_route(assignment.getOrN(), assignment.getDeN(), routeSet) #Modificação do arquivo c++
        routeSet = self.parent.topology.getRoutes(assignment.getOrN(), assignment.getDeN()) #Modificação do arquivo c++

        #Routing.Yen(assignment.getOrN(), assignment.getDeN(), parent.routing.KYEN)

        # Comentando porque só há uma rota
        #for route in routeSet.Path:
        netLayer = self.parent.topology.checkSlotNumberDisp(routeSet, assignment.getNumSlots()) #TODO: ERRO AQUI
        phyLayer = self.parent.topology.checkOSNR(routeSet, assignment.getOSNRth())

        if(netLayer and phyLayer):
            assignment.setRoute(routeSet)
        
    ## ************* Heuristicas para roteamento RWA ***************** ##
    def spectrum_allocation(self, assignment: Assignment) -> None:

        if FF_code == self.parent.definitions.alocation_algorithm:
            self.FirstFit(assignment)
        if RD_code == self.parent.definitions.alocation_algorithm:
            self.Random(assignment)


    def FirstFit(self, assignment) -> None:
        route = assignment.getRoute()
        numSlotsReq = assignment.getNumSlots()
        sumSlots = 0

        for slot in range(self.parent.topology.get_num_slots() - numSlotsReq + 1):
            if self.parent.topology.checkSlotDisp(route, slot):
                sumSlots += 1
                if sumSlots == numSlotsReq:
                    # Dessa forma o algoritmo está iniciando pelo valor final e somando a partir dali, perdendo o espaço do inicio. #TODO: Mudar isso
                    assignment.setSlot_inic(slot - numSlotsReq + 1)
                    assignment.setSlot_fin(slot)
                    break
            else:
                sumSlots = 0
        

    def Random(self, assignment) -> None:
        route = assignment.getRoute() # Armazena a rota que está solicitando uma requisição.

        numSlotsReq = assignment.getNumSlots() # Tamanho dos slots necessários para comportar a solicitação

        route_links = self.parent.topology.get_links(route) # Coleta todos os links que formam a rota

        # Encontra os únicos slots livres que comportam a sequência de slots necessários para a requesição
        #TODO: Fazer una junção para quando um dos slots estiver ocupado já definir o slot como ocupado
        slots_avalable = self.parent.topology.get_slots_avalable(route_links)

        # slots_avalable = ''.join([str(slot) for slot in slots_avalable])

        # Todos os slots iniciais que podem armazenar a requição
        first_slots_avalable = []
        for index_slot_start in range(self.parent.topology.get_num_slots() - numSlotsReq):

            numContiguousSlots = 0

            for index_slot_end in range(numSlotsReq):
                if slots_avalable[index_slot_start + index_slot_end] == SLOT_FREE:
                    numContiguousSlots += 1
                else:
                    break
            if numContiguousSlots == numSlotsReq:
                first_slots_avalable.append(index_slot_start)              

        slot_initial = sample(first_slots_avalable, 1)[0]  

         
        assignment.setSlot_inic(slot_initial)
        assignment.setSlot_fin(slot_initial + numSlotsReq - 1)

        pass

    def ExpandConnection(self, con) -> None:
        #Expand an edge slot according to the following policy:
        self.ExpandRandomly(con) # Remove o slot da direita ou da esquerda com igual probabilidade.


    def ExpandRandomly(self, con) -> None: # Remove aleatoriamente o slot da direita ou da esquerda.
        if(random.randint(0, RAND_MAX) % 2 == 0):
            con.expandLeft() # Expand to the left
        else:
            con.expandRight() # Expand to the rigth
    

    def CompressConnection(self, con) -> None:
        """Compress an edge slot according to the following policy:

        Args:
            con (Connection): Conexão
        """
        self.CompressRandomly(con) #Remove o slot da direita ou da esquerda com igual probabilidade.
    

    def CompressRandomly(self, con) -> None:
        """Remove aleatoriamente o slot da direita ou da esquerda.

        Args:
            con (Connection): Conexão
        """
        if(random.randint(0, RAND_MAX) % 2 == 0): # Compress to the left
            con.compressLeft()
        else:
            con.compressRight() # Compress to the rigth;
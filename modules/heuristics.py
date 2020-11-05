
import random
from random import sample
from modules.settings import RAND_MAX, SLOT_FREE, SpectrumCode, TiebreakerAlgorithm
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

        if SpectrumCode.FirstFit.value == self.parent.definitions.alocation_algorithm:
            starting_slot, final_slot  = self.FirstFit(assignment)
        if SpectrumCode.Random.value == self.parent.definitions.alocation_algorithm:
            starting_slot, final_slot  = self.Random(assignment)
        if SpectrumCode.MostUsed_FirstFit.value == self.parent.definitions.alocation_algorithm:
            starting_slot, final_slot  = self.Used(assignment, is_most_used = True, tiebreaker_algorithm = TiebreakerAlgorithm.FirstFit)
        if SpectrumCode.MostUsed_Random.value == self.parent.definitions.alocation_algorithm:
            starting_slot, final_slot  = self.Used(assignment, is_most_used = True, tiebreaker_algorithm = TiebreakerAlgorithm.Random)
        if SpectrumCode.LeastUsed_FirstFit.value == self.parent.definitions.alocation_algorithm:
            starting_slot, final_slot  = self.Used(assignment, is_most_used = False, tiebreaker_algorithm = TiebreakerAlgorithm.FirstFit)
        if SpectrumCode.LeastUsed_Random.value == self.parent.definitions.alocation_algorithm:
            starting_slot, final_slot  = self.Used(assignment, is_most_used = False, tiebreaker_algorithm = TiebreakerAlgorithm.Random)


        # Valia se os slots são validos e insere
        if (starting_slot != -1) and (final_slot != -1):
            assignment.setSlot_inic(starting_slot)
            assignment.setSlot_fin(final_slot)


    def FirstFit(self, assignment: Assignment) -> tuple:
        """Algoritmo FirstFit. Seleciona o primeiro slot disponivel para a rota

        Args:
            assignment (Assignment): Pedido de requisição

        Returns:
            tuple: Slot inicial e slot final
        """
        route = assignment.getRoute()
        num_slots_req = assignment.getNumSlots()

        # 0 significa que o slot está livre
        busy_slots= [0 for _ in range(self.parent.topology.get_num_slots())]

        for link in route.links:
            for index_slot, slot_by_link in enumerate(link.Status):
                busy_slots[index_slot] |= slot_by_link

        current_free_slots = 0

        for index_slot in range(self.parent.topology.get_num_slots() - num_slots_req + 1):
            if not busy_slots[index_slot]:
                current_free_slots += 1
            else:
                current_free_slots = 0
            
            if current_free_slots == num_slots_req:
                return (index_slot - num_slots_req + 1), index_slot

        return -1, -1


    def Random(self, assignment: Assignment) -> None:
        route = assignment.getRoute()
        num_slots_req = assignment.getNumSlots()

        # 0 significa que o slot está livre
        busy_slots= [0 for _ in range(self.parent.topology.get_num_slots())]

        for link in route.links:
            for index_slot, slot_by_link in enumerate(link.Status):
                busy_slots[index_slot] |= slot_by_link

        current_free_slots = 0

        # Todos os slots iniciais que podem armazenar a requição
        first_slots_avalable = []

        for index_slot in range(self.parent.topology.get_num_slots() - num_slots_req + 1):
            if not busy_slots[index_slot]:
                current_free_slots += 1
            else:
                current_free_slots = 0
            
            if current_free_slots >= num_slots_req:
                first_slots_avalable.append(index_slot - num_slots_req + 1) 

        # Verifica se ao menos um slot está disponivel
        if first_slots_avalable != []:

            starting_slot = sample(first_slots_avalable, 1)[0]  
            final_slot = starting_slot + num_slots_req - 1

            return starting_slot, final_slot

        return -1, -1


    def Used(self, assignment: Assignment, is_most_used: bool, tiebreaker_algorithm: TiebreakerAlgorithm) -> None:
        route = assignment.getRoute()
        num_slots_req = assignment.getNumSlots()

        # 0 significa que o slot está livre
        busy_slots = [0 for _ in range(self.parent.topology.get_num_slots())]
        usage_slots = [-1 for _ in range(self.parent.topology.get_num_slots())]

        for link in route.links:
            for index_slot, slot_by_link in enumerate(link.Status):
                busy_slots[index_slot] |= slot_by_link

        usage_slots = self.parent.topology.global_slot_ocupation.copy()

        for index_slot in range(self.parent.topology.get_num_slots()):
            if busy_slots[index_slot] or (index_slot >= self.parent.topology.get_num_slots() - num_slots_req + 1):
                usage_slots[index_slot] = -1

        possible_start_slot = sorted(enumerate(usage_slots), key = lambda value: value[1], reverse = is_most_used)

        starting_slot = -1

        for index_slot, _ in possible_start_slot:

            # Não existem slots disponíveis
            if usage_slots[index_slot] == -1:
                break
            
            # Não há slots suficientes para alocar a requisição
            if index_slot + num_slots_req -1 > self.parent.topology.get_num_slots():
                usage_slots[index_slot] = -1
                continue
            
            # Verifica se os slots sequentes são suficientes para armazenar a requisição
            is_slot_valid = 0
            for slot in range(index_slot, index_slot + num_slots_req):
                is_slot_valid |= busy_slots[slot]
                if is_slot_valid:
                    break
            
            if not is_slot_valid:
                starting_slot = index_slot
            else:
                usage_slots[index_slot] = -1

            if starting_slot != -1:
                break

        if starting_slot != -1:
            final_slot = starting_slot + num_slots_req - 1

            return starting_slot, final_slot

        return -1, -1


    def RCL(self, assignment: Assignment, tiebreaker_algorithm: TiebreakerAlgorithm) -> None:

        route = assignment.getRoute() # Armazena a rota que está solicitando uma requisição.

        numSlotsReq = assignment.getNumSlots() # Tamanho dos slots necessários para comportar a solicitação

        # Verifica os status da rota 
        route_status = route.get_count_slot_unable()
        
        # Todos os slots iniciais que podem armazenar a requição junto com a sua pontuação
        alocation_slot_score = []
        for index_slot_start in range(self.parent.topology.get_num_slots() - numSlotsReq + 1):

            numContiguousSlots = 0

            for index_slot_end in range(numSlotsReq):
                if route_status[index_slot_start + index_slot_end] == 0:
                    numContiguousSlots += 1
                else:
                    break

            if numContiguousSlots == numSlotsReq:
                # Calcula o score do intervalo de slots
                points = sum([self.parent.topology.global_slot_ocupation[index] for index in range(index_slot_start, index_slot_start + index_slot_end + 1)])
                #Armazena o slot inicial e o score do conjunto necessário para alocar a requisição
                alocation_slot_score.append((index_slot_start, points))  


    
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

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
            self.FirstFit(assignment)
        if SpectrumCode.Random.value == self.parent.definitions.alocation_algorithm:
            self.Random(assignment)
        if SpectrumCode.MostUsed_FirstFit.value == self.parent.definitions.alocation_algorithm:
            self.Used(assignment, is_most_used = True, tiebreaker_algorithm = TiebreakerAlgorithm.FirstFit)
        if SpectrumCode.MostUsed_Random.value == self.parent.definitions.alocation_algorithm:
            self.Used(assignment, is_most_used = True, tiebreaker_algorithm = TiebreakerAlgorithm.Random)
        if SpectrumCode.LeastUsed_FirstFit.value == self.parent.definitions.alocation_algorithm:
            self.Used(assignment, is_most_used = False, tiebreaker_algorithm = TiebreakerAlgorithm.FirstFit)
        if SpectrumCode.LeastUsed_Random.value == self.parent.definitions.alocation_algorithm:
            self.Used(assignment, is_most_used = False, tiebreaker_algorithm = TiebreakerAlgorithm.Random)


    def FirstFit(self, assignment: Assignment) -> None:
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
        

    def Random(self, assignment: Assignment) -> None:
        route = assignment.getRoute() # Armazena a rota que está solicitando uma requisição.

        numSlotsReq = assignment.getNumSlots() # Tamanho dos slots necessários para comportar a solicitação

        route_links = self.parent.topology.get_links(route) # Coleta todos os links que formam a rota

        # Encontra os únicos slots livres que comportam a sequência de slots necessários para a requesição
        slots_avalable = self.parent.topology.get_slots_avalable(route_links)

        # Todos os slots iniciais que podem armazenar a requição
        first_slots_avalable = []
        for index_slot_start in range(self.parent.topology.get_num_slots() - numSlotsReq + 1):

            numContiguousSlots = 0

            for index_slot_end in range(numSlotsReq):
                if slots_avalable[index_slot_start + index_slot_end] == SLOT_FREE:
                    numContiguousSlots += 1
                else:
                    break
            if numContiguousSlots == numSlotsReq:
                first_slots_avalable.append(index_slot_start)              

        # Verifica se ao menos um slot está disponivel
        if first_slots_avalable != []:

            slot_initial = sample(first_slots_avalable, 1)[0]  

            assignment.setSlot_inic(slot_initial)
            assignment.setSlot_fin(slot_initial + numSlotsReq - 1)


    def Used(self, assignment: Assignment, is_most_used: bool, tiebreaker_algorithm: TiebreakerAlgorithm) -> None:
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

        #Verifica se algum slot está disponivel para ser utilizado
        if alocation_slot_score != []:

            # Ordena os slots disponíveis de acordo com o algoritmo usado. Em caso do Most Used será do maior para menor e do Least Used ao contrário.
            alocation_slot_points_order = sorted(alocation_slot_score, key = lambda value: value[1], reverse = is_most_used)

            ### Avaliação para o critério de desempate
            # Cria uma lista somente com os slots de maior pontuação
            best_score = alocation_slot_points_order[0][1]

            # Cria a lista de desempate
            tiebreaker = [start_slot for start_slot, score in alocation_slot_points_order if score == best_score]

            # Escolhe de acordo com o desempate selecionado
            if tiebreaker_algorithm == TiebreakerAlgorithm.FirstFit:
                # Retorna o primeiro
                slot_initial = tiebreaker[0]

                assignment.setSlot_inic(slot_initial)
                assignment.setSlot_fin(slot_initial + numSlotsReq - 1)

            if tiebreaker_algorithm == TiebreakerAlgorithm.Random:
                # Seleciona um com igual probabilidade
                slot_initial = sample(tiebreaker, 1)[0]  

                assignment.setSlot_inic(slot_initial)
                assignment.setSlot_fin(slot_initial + numSlotsReq - 1)
 
    
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
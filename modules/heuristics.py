
import random
from modules.settings import RAND_MAX

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

    ## Heuristicas para roteamento RWA
    def FirstFit(self, assignment) -> None:
        route = assignment.getRoute()
        numSlotsReq = assignment.getNumSlots()
        sumSlots = 0

        for slot in range(self.parent.topology.get_num_slots() - numSlotsReq + 1):
            if self.parent.topology.checkSlotDisp(route, slot):
                sumSlots += 1
                if sumSlots == numSlotsReq:
                    assignment.setSlot_inic(slot)
                    assignment.setSlot_fin(slot + numSlotsReq - 1)
                    break
            else:
                sumSlots = 0

    def ExpandConnection(self, con) -> None:
        #Expand an edge slot according to the following policy:
        self.ExpandRandomly(con) # Remove o slot da direita ou da esquerda com igual probabilidade.

    def ExpandRandomly(self, con) -> None: # Remove aleatoriamente o slot da direita ou da esquerda.
        if(random.randint(0, RAND_MAX) % 2 == 0):
            con.expandLeft() # Expand to the left
        else:
            con.expandRight() # Expand to the rigth
    
    def CompressConnection(self, con) -> None:
        #Compress an edge slot according to the following policy:
        self.CompressRandomly(con) #Remove o slot da direita ou da esquerda com igual probabilidade.
    
    def CompressRandomly(self, con) -> None:# Remove aleatoriamente o slot da direita ou da esquerda.
        if(random.randint(0, RAND_MAX) % 2 == 0): # Compress to the left
            con.compressLeft()
        else:
            con.compressRight() # Compress to the rigth;
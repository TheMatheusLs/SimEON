import json
from modules.link import Link
from modules.route import Route
from modules.signal import Signal
from modules.settings import SLOT_USED, SLOT_FREE

class Topology:
    def __init__(self, topology_path, parent, *args, **kwargs) -> None:

        self.parent = parent

        # Todas as informações da topologia e salva em 'topology_info'
        try:
            with open(topology_path) as topology_file:
                topology_info = json.load(topology_file)

            #Adquire o número de slots
            self.num_slots = topology_info["NumberOfSlots"]

            # Adquire o número de nós
            self.setNumNodes(topology_info["NumberOfNodes"])
            
            # Adquire o número de enlaces
            self.num_links = topology_info["NumberOfLinks"]


            print(f"Number Of Nodes: {self.num_nodes}")
            print(f"Number Of Links: {self.num_links}")
            print(f"Number Of Slots: {self.num_slots}")
            
            self.links = []	

            for info_link in topology_info["Links"]:
                origin_node = info_link["OriginNode"]
                destination_node = info_link["DestinationNode"]
                length = info_link["LinkLength"]
                num_sections = info_link["NumberOfSections"]

                link = Link(origin_node, destination_node, length, num_sections, self)

                if self.valid_link(link):
                    self.insert_link(link)
                    
        except Exception as e:
            print(f"Could not load topology. {e}")


    def initialise(self) -> None:
        """ Inicializa a topologia da rede
        """
        for o_node in range(self.num_nodes):
            for d_node in range(self.num_nodes):    
                if self.linkTopology[o_node * self.num_nodes + d_node] != None:
                    self.linkTopology[o_node * self.num_nodes + d_node].initialise()


    def printAllRoutes(self) -> None:
        """Escreve todas as rotas no console
        """
        for o_node in range(self.num_nodes):
            for d_node in range(self.num_nodes):
                if o_node != d_node:
                    print(f"\n[origin Node = {o_node}  destination Node = {d_node}]")
                    for p in range(len(self.getRoutes(o_node, d_node).Path)):
                        print(f"Route({p}): ", end=' ')
                        route = self.getRoutes(o_node, d_node).Path
                        self.printRoute(route)
                        break ## Forcando a sair do loop para ficar igual a simulação do codeblocks


    def printRoute(self, route: Route) -> None:
        """Escreve uma rota no console

        Args:
            route (Route): Rota a ser mostrada no console
        """
        hops = len(route) - 1
        print(f"hops = {hops}: ", end='')
        for h in range(hops + 1):
            print(route[h], end=" - " if h != hops else '')
        print()


    def setNumNodes(self, num_nodes: int) -> None:
        """Configura o número de nós, carrega a topologia e os nós em funcionamento

        Args:
            num_nodes (int): Número de nós na rede
        """
        self.num_nodes =  num_nodes

        self.linkTopology = [None for _ in range(self.num_nodes * self.num_nodes)]

        self.NodeWorking =  []

        for i_node in range(self.num_nodes):
            self.NodeWorking.append(True)

            for j_node in range(self.num_nodes):
                self.linkTopology[i_node * self.num_nodes + j_node] = None #Link(parent = self)

        self.AllRoutes = [None for _ in range(self.num_nodes * self.num_nodes)]


    def clearRoutes(self, origin_node: int, destination_node: int) -> None:
        """Limpa as rotas entre o nó de origem e destinos

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino
        """
        self.AllRoutes[origin_node * self.num_nodes + destination_node] = None


    def getRoutes(self, origin_node: int, destination_node: int) -> Route:
        """Retorna as rotas entre a origem e o destino

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino

        Returns:
            Route: Rotas
        """
        return self.AllRoutes[origin_node * self.num_nodes + destination_node]


    def set_route(self, origin_node: int, destination_node: int, route: Route) -> None:
        """Adiciona a rota entre a origem e o destino

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino
            route (Route): Rota a ser adicionadas       
        """
        self.clearRoutes(origin_node, destination_node)
        self.addRoute(origin_node, destination_node, route)


    def addRoute(self, origin_node: int, destination_node: int, route: Route) -> None:
        """Adiciona uma rota 

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino
            route (Route): Rota
        """
        self.AllRoutes[origin_node * self.num_nodes + destination_node] = route


    def getLink(self, origin_node: int, destination_node: int) -> Link:
        """Recupera o link entre dois nós

        Args:
            origin_node (int): Nó de origem
            destination_node (int): Nó de destino

        Returns:
            Link: Link retornado
        """
        if not (self.valid_node(origin_node) and self.valid_node(destination_node)):
            print(f"Error in Topology::getLink() {origin_node} {destination_node}")
        return self.linkTopology[origin_node * self.num_nodes + destination_node]


    def insert_link(self, link: Link) -> None:
        """Insere um link na topologia

        Args:
            link (Link): Link para ser inserido
        """
        if self.valid_link(link):
            self.linkTopology[link.get_origin_node() * self.num_nodes + link.get_destination_node()] = link
    

    def isNodeWorking(self, node: int) -> bool:
        """Verifica se o nó está em funcionamento

        Args:
            node (int): Nó para ser verificado

        Returns:
            bool: Verdadeiro caso o nó esteja em funcionamento
        """
        return self.NodeWorking[node]


    def valid_node(self, node: int) -> bool:
        """Verifica se um nó é válido

        Args:
            node (int): Nó a ser verificado

        Returns:
            bool: Verdadeiro se o nó for válido
        """
        return (node >= 0 and node < self.get_num_nodes())


    def valid_link(self, link: Link) -> bool:
        """Verifica se um link é válido

        Args:
            link (Link): Link a ser verificado

        Returns:
            bool: Verdadeiro se o link for válido
        """
        return ( self.valid_node(link.get_origin_node()) and self.valid_node(link.get_destination_node()) )


    def get_num_nodes(self) -> int:
        """Retorna o número de nós

        Returns:
            int: Número de nós
        """
        return self.num_nodes


    def get_num_links(self) -> int:
        """Retorna o número de links

        Returns:
            int: Número de links
        """
        return self.num_links


    def get_num_slots(self) -> int:
        """Retorna o número de slots

        Returns:
            int: Número de slots
        """
        return self.num_slots


    def checkSlotDisp(self, route: Route, slot: int) -> bool:

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or, L_de)

            if self.valid_link(link):
                pass

            if link.isSlotOccupied(slot):
                return False
        return True


    def checkSlotNumberDisp(self, route: Route, numSlots: int):
        numContiguousSlots = 0

        for slot in range(self.get_num_slots() - numSlots): # Só está olhando o número de slot da requisição. Modificando para olhar em todos os slots da rota
            if self.checkSlotDisp(route, slot):
                numContiguousSlots += 1
            else:
                numContiguousSlots = 0
            
            if numContiguousSlots == numSlots:
                return True
        return False
    

    def checkOSNR(self, route, OSNRth):

        signal = Signal(self)
        signal.initialise()

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or,L_de)
            link.calcSignal(signal)
        
        if(signal.getOSNR() > OSNRth):
            return True
        return False


    def connect(self, connection) -> None:
        #Insert connection into the network
        route = connection.getRoute()

        for c in range(route.getNumHops()):
            if self.valid_node(route.getNode(c)):
                L_or = route.getNode(c)
                L_de = route.getNode(c+1)
                link = self.getLink(L_or, L_de)
                assert(self.valid_link(link))

                for slot in range(connection.getFirstSlot(), connection.getLastSlot() + 1):
                    link.occupySlot(slot) # Aqui o slot é ocupado

        self.parent.definitions.numHopsPerRoute += route.getNumHops()
        self.parent.definitions.netOccupancy += ((connection.getLastSlot() - connection.getFirstSlot() + 1) * route.getNumHops())
    

    def releaseConnection(self, connection) -> None: #Connection* conn0x622ef00x622ef0ection
        route = connection.getRoute()
        #release all slots used for the Connection

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or, L_de)
            assert(self.valid_link(link)) #Acrescentei

            for slot in range(connection.getFirstSlot(), connection.getLastSlot() + 1):
                link.releaseSlot(slot)


    def releaseSlot(self, connection, slot: int) -> None: #Release slot s in all links of connection
        route = connection.getRoute()
        #release all slots used for the Connection

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c+1)
            link = self.getLink(L_or, L_de)
            link.releaseSlot(slot)


    def occupySlot(self, connection, slot: int) -> None: # occupy slot s in all links of connection
        #Insert connection into the network
        route = connection.getRoute()

        for c in range(route.getNumHops()):
            L_or = route.getNode(c)
            L_de = route.getNode(c + 1)
            link = self.getLink(L_or, L_de)
            link.occupySlot(slot)
        
        
    def areThereOccupiedSlots(self) -> bool:
        #if (self.valid_link(link)):
        for origin_node in range(self.num_nodes):
            for destination_node in range(self.num_nodes):
                link = self.linkTopology[origin_node * self.num_nodes + destination_node]

                if link != None: #There is a link between nodes oN and dN
                    for slot in range(self.get_num_slots()):
                        if link.isSlotOccupied(slot):
                            return True
        return False


    def get_links(self, route: Route) -> list:
        """Retorna os links que constroem a rota informada

        Args:
            route (Route): Rota

        Returns:
            list: Links que formam a rota 
        """
        links = []

        for node in range(route.getNumHops()):
            link_origin = route.getNode(node)
            link_destination = route.getNode(node + 1)
            link = self.getLink(link_origin, link_destination)
            if self.valid_link(link):
                links.append(link)

        return links

    
    def get_slots_avalable(self, links: Link) -> list:

        slots = []

        for index_slot in range(self.get_num_slots()):
            slots.append(None)
            for link in links:
                if not link.isSlotFree(index_slot):
                    slots[index_slot] = SLOT_USED
                    break
            if slots[index_slot] == None:
                slots[index_slot] = SLOT_FREE                    

        return slots
    
    def get_all_routes(self) -> list:
        """Retorna a lista com todas as rotas armazenadas na topologia

        Returns:
            list: Lista das rotas
        """
        return self.AllRoutes

    def create_conflict_routes(self) -> None:

        for route in self.get_all_routes():
            if route != None:
                route.set_conflict_routes()
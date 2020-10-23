import json
from modules.link import Link


class Topology:
    def __init__(self, topology_path, parent, *args, **kwargs) -> None:

        self.parent = parent

        self.RouteInt = []

        # Todas as informações da topologia e salva em 'topology_info'
        try:
            with open(topology_path) as topology_file:
                topology_info = json.load(topology_file)

            # Adquire o número de nós
            self.setNumNodes(topology_info["NumberOfNodes"])
            
            # Adquire o número de enlaces
            self.num_links = topology_info["NumberOfLinks"]

            #Adquire o número de slots
            self.num_slots = topology_info["NumberOfSlots"]

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

    def initialise(self):
        for o_node in range(self.num_nodes):
            for d_node in range(self.num_nodes):    
                if self.linkTopology[o_node * self.num_nodes + d_node] != None:
                    self.linkTopology[o_node * self.num_nodes + d_node].initialise()

    def printAllRoutes(self) -> None:

        for o_node in range(self.num_nodes):
            for d_node in range(self.num_nodes):
                if o_node != d_node:
                    print(f"\n[origin Node = {o_node}  destination Node = {d_node}]")
                    for p in range(len(self.getRoutes(o_node, d_node).Path)):
                        print(f"Route({p}): ", end='')
                        route = self.getRoutes(o_node, d_node).Path
                        self.printRoute(route)

    def printRoute(self, route):
        hops = len(route)
        print(f"hops = {hops}: ")
        for h in range(hops):
            print(route[h])


    def setNumNodes(self, num_nodes):

        self.num_nodes =  num_nodes

        self.linkTopology = [Link for _ in range(self.num_nodes * self.num_nodes)]

        self.NodeWorking =  []

        for i_node in range(self.num_nodes):
            self.NodeWorking.append(True)

            for j_node in range(self.num_nodes):
                self.linkTopology[i_node * self.num_nodes + j_node] = None

        self.AllRoutes = [None for _ in range(self.num_nodes * self.num_nodes)]

    def clearRoutes(self, origin_node, destination_node):
        self.AllRoutes[origin_node * self.num_nodes + destination_node] = None

    def getRoutes(self, origin_node, destination_node):
        return self.AllRoutes[origin_node * self.num_nodes + destination_node]

    def set_route(self, origin_node, destination_node, route):
        self.clearRoutes(origin_node, destination_node)
        self.addRoute(origin_node, destination_node, route)

    def addRoute(self, origin_node, destination_node, route) -> None:
        self.AllRoutes[origin_node * self.num_nodes + destination_node] = route

    def getLink(self, origin_node: int, destination_node: int) -> None:
        if not (self.valid_node(origin_node) and self.valid_node(destination_node)):
            print(f"Error in Topology::getLink() {origin_node} {destination_node}")
            #TODO: Implementar o array linktopology no momento de construir a topologia
        return self.linkTopology[origin_node * self.num_nodes + destination_node]

    def insert_link(self, link: Link) -> None:
        if self.valid_link(link):
            self.linkTopology[link.get_origin_node() * self.num_nodes + link.get_destination_node()] = link
    
    def isNodeWorking(self, node: int) -> bool:
        return self.NodeWorking[node]

    def valid_node(self, node: int) -> bool:
        return (node >= 0 and node < self.get_num_nodes())

    def valid_link(self, link: Link) -> bool:
        return ( self.valid_node(link.get_origin_node()) and self.valid_node(link.get_destination_node()) )

    def get_num_nodes(self) -> int:
        return self.num_nodes
        
    def get_num_links(self) -> int:
        return self.num_links

    def get_num_slots(self) -> int:
        return self.num_slots
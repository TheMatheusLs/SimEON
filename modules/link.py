
from modules.settings import SLOT_USED, SLOT_FREE, LinkCostType


class Link:
    def __init__(self, origin_node: int, destination_node: int, length: float, num_sections: int, parent, *args, **kwargs) -> None:

        self.parent = parent

        self.origin_node = origin_node
        self.destination_node = destination_node
        self.length = length
        self.num_sections = num_sections

        self.isBroken = False

        self.Status = None

        self.linkCostType = LinkCostType.minHops
    

    def setAsBroken(self) -> None:
        """Configura o link como quebrado
        """
        self.isBroken = True

    def setAsWorking(self) -> None:
        """Configura o link como funcionando
        """
        self.isBroken = False

    def getCost(self) -> float:
        """Retorna o custo do link a depender da métrica escolhida

        Returns:
            float: Custo do link
        """
        if self.isBroken:
            return float('inf')

        if self.linkCostType == LinkCostType.minHops: #Assuming MinHops
            return 1.0
        else:
            if self.linkCostType == LinkCostType.minLength: #Assuming MinDist
                return self.length
            else:
                raise ValueError("A métrica usada está incompátivel")
        
    def initialise(self) -> None:
        """Inicia o link com todos os slots livres
        """
        self.Status = [SLOT_FREE for _ in range(self.parent.num_slots)]

    def get_origin_node(self) -> int:
        """Retorna o nó de origem

        Returns:
            int: Nó de origem
        """
        return self.origin_node

    def get_destination_node(self) -> int:
        """Retorna o nó de destino

        Returns:
            int: Nó de destino
        """
        return self.destination_node
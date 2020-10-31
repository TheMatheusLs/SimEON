TOPOLOGY_PATH = ".\\others\\topology.json"

TRAFFIC_PATH = ".\\others\\traffic.json"

SLOT_FREE = 0
SLOT_USED = 1

SEED = 42 # Semente aleátoria
RAND_MAX = 32767 # Máximo valor que o rand pode retornar

ROLLOFF = 0.0
   
RANDOM_SEED = 42

from enum import Enum, auto

class RoutingCode(Enum):
    Dijkstra = auto()

class SpectrumCode(Enum):
    Random = auto()
    FirstFit = auto()
    MostUsed_Random = auto()
    MostUsed_FirstFit = auto()
    LeastUsed_Random = auto()
    LeastUsed_FirstFit = auto()

class TiebreakerAlgorithm(Enum):
    FirstFit = auto()
    Random = auto()

class LinkCostType(Enum):
    minHops = auto()
    minLength = auto()

class EventType(Enum):
    UNKNOWN = auto()
    Req = auto()
    Desc = auto()
    Exp = auto()
    Comp = auto()
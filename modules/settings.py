TOPOLOGY_PATH = ".\\others\\topology.json"

TRAFFIC_PATH = ".\\others\\traffic.json"

DJK_code = 0
YEN_code = 1

RD_code = 0
FF_code = 1

SLOT_FREE = 0
SLOT_USED = 1

SEED = 42 # Semente aleátoria
RAND_MAX = 32767 # Máximo valor que o rand pode retornar

ROLLOFF = 0.0
   
RANDOM_SEED = 42

from enum import Enum, auto

class LinkCostType(Enum):
    minHops = auto()
    minLength = auto()

class EventType(Enum):
    UNKNOWN = auto()
    Req = auto()
    Desc = auto()
    Exp = auto()
    Comp = auto()
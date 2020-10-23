TOPOLOGY_PATH = ".\\others\\topology.json"

TRAFFIC_PATH = ".\\others\\traffic.json"

DJK_code = 0
YEN_code = 1

RD_code = 0
FF_code = 1

SLOT_FREE = 0
SLOT_USED = 1

from enum import Enum, auto

class LinkCostType(Enum):
    minHops = auto()
    minLength = auto()
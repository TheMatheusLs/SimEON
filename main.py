import json                         # Importa o modulo para trabalhar com arquivos .json
from modules.settings import *      # Modulo com as configurações e as constantes usadas ao logo do código
from modules.topology import *      # Modulo para armazenar e manipular a topologia da rede
from modules.traffic import *       # Modulo para armazenar e manipular a tráfego da rede
from modules.definitions import *   # Modulo para armazenar e manipular as definições
from modules.schedule import *      # Modulo controlar a execução do tempo
from modules.routing import *       # Modulo

class Main:
    def __init__(self, *args, **kwargs) -> None:

        # Cria os objetos para cada classe
        self.topology = Topology(TOPOLOGY_PATH, self)
        self.traffic = Traffic(TRAFFIC_PATH, self)
        self.definitions = Definitions(self)
        self.schedule = Schedule(self)

        # Inicializa todas as classes
        self.topology.initialise()
        self.definitions.initialise()
        self.schedule.initialise()

        # Encontra as todas as rotas usando o algoritmo escolhido
        self.routing = Routing(self.definitions.routing_algorithm, self)

        # Escreve todas as rotas na tela
        self.topology.printAllRoutes()

if __name__ == "__main__":
    
    Main()

    print("Start Of Simulation: ")
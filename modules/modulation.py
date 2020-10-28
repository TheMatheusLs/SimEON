
from modules.settings import ROLLOFF

def bandwidthQAM(M: int, Rbps: float, pol: float) -> float:
    return ((1.0 + ROLLOFF)* Rbps) / (pol * M)

def getSNRbQAM(M: int, ber: float) -> float:
    return 0 #TODO: Arruamar essa função as modulações não estão sendo aplicada corretamente. Sempre irá retornar 0

    if((ber > 3.799 * (10.0 ** (-3))) and (ber < 3.801 * (10.0 ** (-3)))):
        if M == 2: #QAM-4
            return 6.79
        if M == 3: #QAM-8
            return 9.03
        if M == 4: #QAM-16
            return 10.52
        if M == 5: #QAM-32
            return 12.57
        if M == 6: #QAM-64
            return 14.77
        else:
            print("Unknown Modulation Format")  
    else:
        if((ber > 3.799 * (10.0 ** (-3))) and (ber < 3.801 * (10.0 ** (-3)))):
            if M == 2: #QAM-4
                return 5.52
            if M == 3: #QAM-8
                return 7.83
            if M == 4: #QAM-16
                return 9.17
            if M == 5: #QAM-32
                return 11.23
            if M == 6: #QAM-64
                return 13.34
            else:
                print("Unknown Modulation Format")
    print("Problem in Modulation::getSNRbQAM")
    return 0.0

def getsnrbQAM(M: int, ber: float):
    print("Modulation::Consertar isso aqui")
    return 0.0

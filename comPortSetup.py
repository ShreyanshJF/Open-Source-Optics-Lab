from serial.tools import list_ports


def getComportsList():
    allComPorts = list_ports.comports()
    out = []
    for i in allComPorts:
        com = {
            "device": i.device,
            "name": i.name,
            "manufacturer": i.manufacturer,
            "description": i.description
        }
        out.append(com)
    return out

import re
def dijkstra(persona,esquinas):
    vertices=esquinas.keys()
    pos=persona.getPos()
    nodos={}
    posx=re.search("(e\d+),(\d+)",pos[0])
    posy=re.search("(e\d+),(\d+)",pos[1])
    print(f"x:{posx.group(1)},dx:{posx.group(2)}\ny:{posy.group(1)},dy:{posy.group(2)}")
    nodos[persona.nombre]=0
    for esquina in esquinas:
        nodos[esquina]="inf"
    nodos[esquina]=posx.group(2)
    nodos[esquina]=posy.group(2)
    nodosNoVistos=[n for n in vertices]
    #Si la calle es de 2 direcciones
    if posx.group(1) in esquinas[posy.group(1)].vecinas.keys():
        #Me fijo cual lado es el mas corto para llegar
        #El que sea el mas corto, lo saco de la lista para revisar
        if float(posy.group(2))<float(posx.group(2)):
            node=posy.group(1)
        else:
            node=posx.group(1)
    else:
        node=posx.group(1)
    nodosNoVistos.remove(node)
    nextNodes=esquinas[node].desde
    print("pausa")
    return
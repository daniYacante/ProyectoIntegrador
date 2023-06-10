import re
def dijkstra(persona, esquinas):
    vertices = esquinas.keys()
    pos = persona.getPos()
    nodos = {}
    anteriores = {}  # Diccionario para almacenar los nodos anteriores en el camino
    posx = re.search("(e\d+),(\d+)", pos[0])
    posy = re.search("(e\d+),(\d+)", pos[1])
    print(f"x:{posx.group(1)},dx:{posx.group(2)}\ny:{posy.group(1)},dy:{posy.group(2)}")
    nodos[persona.nombre] = 0

    for esquina in esquinas:
        nodos[esquina] = float('inf')
    nodos[esquina] = int(posx.group(2))
    nodos[esquina] = int(posy.group(2))
    nodosNoVistos = [n for n in vertices]

    # Si la calle es de 2 direcciones
    if posx.group(1) in esquinas[posy.group(1)].vecinas.keys():
        # Me fijo cual lado es el mas corto para llegar
        # El que sea el mas corto, lo saco de la lista para revisar
        if int(posy.group(2)) < int(posx.group(2)):
            node = posy.group(1)
        else:
            node = posx.group(1)
    else:
        node = posx.group(1)
    nodosNoVistos.remove(node)
    nextNodes = esquinas[node].desde
    print("pausa")

    while nodosNoVistos:
        for vecino in nextNodes:
            if vecino in nodosNoVistos:
                newCost = nodos[node] + esquinas[node].vecinas[vecino].distancia
                if newCost < nodos[vecino]:
                    nodos[vecino] = newCost
                    anteriores[vecino] = node  # Actualiza el nodo anterior

        minNode = None
        for n in nodosNoVistos:
            if nodos[n] != float('inf'):
                if minNode is None or nodos[n] < nodos[minNode]:
                    minNode = n
        if minNode is None:
            break
        node = minNode
        nodosNoVistos.remove(node)
        nextNodes = esquinas[node].desde

    # Construye el camino en reversa utilizando los nodos anteriores
    camino_reversa = []
    nodo_actual = esquina
    while nodo_actual in anteriores:
        camino_reversa.append(nodo_actual)
        nodo_actual = anteriores[nodo_actual]
    camino_reversa.append(nodo_actual)

    return nodos, list(reversed(camino_reversa))
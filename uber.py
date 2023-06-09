import argparse
from typing import Dict
import re
import pickle
def serializar(objeto,nombre):
    try:
        with open(nombre,'bw') as f:
            pickle.dump(objeto,f)
    except Exception as e:
        print(e)
        return False
    finally:
        return True
def deserializar(nombre):
    try:
        with open(nombre,'br') as f:
            obj=pickle.load(f)
    except Exception as e:
        print(e)
        return None
    finally:
        return obj

def loadMap(dir:str):
    with open(dir,'r') as mp:
        E=mp.readline().split("=")[1][1:-2].split(",")
        V=re.findall("<e\d+,e\d+,\d+>", mp.readline())
    myMap=mapa(E,V)
    # for i in range(len(myMap.esquinas)):
    #     print(myMap.esquinas[i].name)
    if serializar(myMap,"grafMap"):
        print("Map created successfully")
def loadElm(element:str):
    # Expresion regular que encuentra el objeto y las dos partes de la direccion
    patt=re.compile("([A-Z]\d+),{(<.*>),(<.*>)},*(\d+)*")
    mat=re.search(patt,element)
    elm=mat.group(1,2,3)
    # print(mat.group(1))
    # print(mat.group(2))
    # print(mat.group(3))
    myMap=deserializar("grafMap")
    if myMap==None:
        return
    # Verificar si el nombre del elemento es válido
    if not elm[0].isalnum():
        print('Error: El nombre del elemento solo puede contener caracteres alfanuméricos.')
        return
    # elemento=element[0]
    # direction=element[1]
    # Analizar la dirección y extraer los datos
    # pattern = r'<([a-zA-Z]+), (\d+)>'
    # matches = re.findall(pattern, direction)
    if len(elm) != 3:
        print('Error: La dirección debe consistir en dos tuplas.')
        return
    # Crear las tuplas de dirección
    # dir1 = (matches[0][0], int(matches[0][1]))
    # dir2 = (matches[1][0], int(matches[1][1]))
    dir1=elm[1]
    dir2=elm[2]
    if not myMap.checkDir(dir1,dir2):
        print("Direccion no valida")
        return
    # Verificar si el nombre del elemento ya está en uso
    fij=myMap.getFijos()
    mov=myMap.getMoviles()
    if elm[0] in fij.keys() or elm[0] in mov.keys():
        print(f'Error: El nombre del elemento "{element}" ya está en uso.')
        return
    #Si existe monto es un objeto movil
    if mat.group(4)!=None:
        # Verificar si el monto es un valor numérico
        try:
            monto = float(mat.group(4))
        except ValueError:
            print('Error: El monto debe ser un valor numérico.')
            return
        # Crear el elemento móvil y mostrar información
        movil = elmMovil(elm[0], [dir1, dir2], monto)
        # Actualizar el conjunto de nombres utilizados
        # myMap.moviles[elm[0]]=movil
        myMap.load(movil)
        print(f'Se ha cargado el elemento móvil: {movil.nombre} - {movil.direccion} - Monto: {movil.monto}')
    else:
        fijo = elmFijo(elm[0], [dir1, dir2])
        # Actualizar el conjunto de nombres utilizados
        # myMap.fijos[elm[0]]=fijo
        myMap.load(fijo)
        print(f'Se ha cargado el elemento fijo: {fijo.nombre} - {fijo.direccion}')
    return serializar(myMap,"grafMap")
def createTrip(entrada:str):
    argu=re.search("([A-Z]\d+)\s+(.+)",entrada)
    print(argu.group(1),"--",argu.group(2))

    return
class mapa():
    def __init__(self,E:list,V:list) -> None:
        self.esquinas:Dict[esquina] = {}
        self.fijos:Dict[elmFijo]={}
        self.moviles:Dict[elmMovil]={}
        for vert in E:
            newVert=esquina(vert)
            self.esquinas[vert]=newVert
        for calle in V:
            ex,ey,w=re.findall("e*\d+",calle)
            w=int(w)
            if self.esquinas[ex].name==ex:
                vec=vecina(name=ey,dist=w)
                self.esquinas[ex].vecinas[ey]=vec
                # if ex=="e5" and ey=="e6":
                self.esquinas[ey].desde.append(ex)
                if ey in self.esquinas[ex].shortestPath.keys():
                    if w<self.esquinas[ex].shortestPath[ey]:
                        self.esquinas[ex].shortestPath[ey]=w
                else:
                    self.esquinas[ex].shortestPath[ey]=w
                tablaEy=self.esquinas[ey].shortestPath
                for nodo in tablaEy.keys():
                    if nodo!=ex:
                        if nodo in self.esquinas[ex].shortestPath.keys():
                            if self.esquinas[ex].shortestPath[nodo]>tablaEy[nodo]+w:
                                self.esquinas[ex].shortestPath[nodo]=tablaEy[nodo]+w
                        else:
                            self.esquinas[ex].shortestPath[nodo]=tablaEy[nodo]+w
                for nodosAvisar in self.esquinas[ex].desde:
                    self.esquinas[nodosAvisar].updateDist(self.esquinas[ex].shortestPath,self.esquinas,ex)
    def load(self,elemento):
        if type(elemento)==elmFijo:
            self.fijos[elemento.nombre]=elemento
        else:
            self.moviles[elemento.nombre]=elemento
        # print(elemento.direccion)
        ex=self.getGroups(elemento.direccion[0])
        ey=self.getGroups(elemento.direccion[1])
        calles=self.esquinas[ex.group(1)].vecinas
        if ey.group(1) in calles.keys():
            calles[ey.group(1)].elementos[elemento.nombre]=elemento
        if self.checkDir(elemento.direccion[1],elemento.direccion[0]):
            calles=self.esquinas[ey.group(1)].vecinas
            calles[ex.group(1)].elementos[elemento.nombre]=elemento
    def getFijos(self):
        return self.fijos
    def getMoviles(self):
        return self.moviles
    def getGroups(self,dire):
        d=re.search("(e\d+),(\d+)",dire)
        return d
    def checkDir(self,ex,ey):
        d1=self.getGroups(ex)
        d2=self.getGroups(ey)
        l=int(d1.group(2))+int(d2.group(2))
        calles=self.esquinas[d1.group(1)].vecinas
        if d2.group(1) in calles.keys() and l==int(calles[d2.group(1)].distancia):
            return True
        else:
            return False
class esquina():
    def __init__(self,name:str) -> None:
        self.name=name
        self.vecinas:Dict[vecina]={}
        self.desde=[]
        self.shortestPath={}
    def updateDist(self,tabla:dict,esquinas:dict,hijo):
        d=self.vecinas[hijo].distancia
        NHC=True
        for nodo in tabla.keys():
            if nodo!=self.name:
                if nodo in self.shortestPath.keys():
                    if self.shortestPath[nodo]>tabla[nodo]+d:
                        self.shortestPath[nodo]=tabla[nodo]+d
                        NHC=False
                else:
                    self.shortestPath[nodo]=tabla[nodo]+d
                    NHC=False
        if not NHC:
            for nodosAvisar in self.desde:
                esquinas[nodosAvisar].updateDist(self.shortestPath,esquinas,self.name)
class vecina():
    def  __init__(self,name:str,dist:int) -> None:
        self.name=name
        self.distancia=dist
        self.elementos:Dict[str]={}
class elmFijo():
    def __init__(self,nombre,direccion) -> None:
        self.nombre=nombre
        self.direccion=direccion
    def getPos(self):
        return self.direccion
class elmMovil(elmFijo):
    def __init__(self, nombre, direccion,monto) -> None:
        super().__init__(nombre, direccion)
        self.monto=monto


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-create_map",help="Path al archivo mapa")
    ap.add_argument("-load_fix_element",help="Cargar elemento fijo")
    ap.add_argument("-load_movil_element",help="Cargar elemento movil")
    ap.add_argument("-create_trip",help="Crea de ser posible un viaje")
    args=vars(ap.parse_args())
    if args["create_map"]!=None:
        print(args["create_map"])
        loadMap(args["create_map"])
    if args["load_fix_element"]!=None:
        print(args["load_fix_element"])
        loadElm(args["load_fix_element"])
    if args["load_movil_element"]!=None:
        print(args["load_movil_element"])
        loadElm(args["load_movil_element"])
    if args["create_trip"]!=None:
        print(args["create_trip"])
        createTrip(args["create_trip"])
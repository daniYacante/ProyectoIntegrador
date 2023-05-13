import argparse
from typing import List
import re
import pickle
def loadMap(dir:str):
    with open(dir,'r') as mp:
        E=mp.readline().split("=")[1][1:-2].split(",")
        V=re.findall("<e\d+,e\d+,\d+>", mp.readline())
    myMap=mapa(E,V)
    # for i in range(len(myMap.esquinas)):
    #     print(myMap.esquinas[i].name)
    try:
        with open("grafMap",'bw') as gm:
            pickle.dump(myMap,gm)
    except Exception as e:
        print(e)
class mapa():
    def fhash(self,key):
        return int(key[1:])-1
    def __init__(self,E:list,V:list) -> None:
        self.esquinas:List[esquina] = [None for e in E]
        self.fijos:List[elmFijo]
        self.moviles:List[elmMovil]
        for vert in E:
            newVert=esquina(vert)
            pos=self.fhash(vert)
            if self.esquinas[pos]==None:
                self.esquinas[pos]=newVert
            else:
                print(f"Error cargando esquina {vert}")
        for calle in V:
            ex,ey,w=re.findall("e*\d+",calle)
            pos=self.fhash(ex)
            if self.esquinas[pos].name==ex:
                vec=vecina(name=ey,dist=w)
                self.esquinas[pos].vecinas.append(vec)
class esquina():
    def __init__(self,name:str) -> None:
        self.name=name
        self.vecinas:List[vecina]=[]
class vecina():
    def  __init__(self,name:str,dist:int) -> None:
        self.name=name
        self.distancia=dist
        self.elementos:List[str]=[]
class elmFijo():
    def __init__(self,nombre,direccion) -> None:
        self.nombre=nombre
        self.direccion=direccion
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
    if args["load_movil_element"]!=None:
        print(args["load_movil_element"])
    if args["create_trip"]!=None:
        print(args["create_trip"])
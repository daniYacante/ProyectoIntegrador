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
    test=re.findall("\w+,{\w+}",element)
    elm=element.split(',')
    myMap=deserializar("grafMap")
    if myMap==None:
        return
    # Verificar si el nombre del elemento es válido
    if not elm[0].isalnum():
        print('Error: El nombre del elemento solo puede contener caracteres alfanuméricos.')
        return
    elemento=element[0]
    direction=element[1]
    # Analizar la dirección y extraer los datos
    pattern = r'<([a-zA-Z]+), (\d+)>'
    matches = re.findall(pattern, direction)
    if len(matches) != 2:
        print('Error: La dirección debe consistir en dos tuplas.')
        return
    # Crear las tuplas de dirección
    dir1 = (matches[0][0], int(matches[0][1]))
    dir2 = (matches[1][0], int(matches[1][1]))
    # Verificar si el nombre del elemento ya está en uso
    if elemento in myMap.fijos or element in myMap.moviles:
        print(f'Error: El nombre del elemento "{element}" ya está en uso.')
        return
    if len(elm)==3:
        # Verificar si el monto es un valor numérico
        try:
            monto = float(monto)
        except ValueError:
            print('Error: El monto debe ser un valor numérico.')
            return
        # Crear el elemento móvil y mostrar información
        movil = elmMovil(elemento, [dir1, dir2], monto)
        # Actualizar el conjunto de nombres utilizados
        myMap.moviles[elemento]=movil
        print(f'Se ha cargado el elemento móvil: {movil.nombre} - {movil.direccion} - Monto: {movil.monto}')
    elif len(elm)==2:
        fijo = elmFijo(elemento, [dir1, dir2])
        # Actualizar el conjunto de nombres utilizados
        myMap.fijos[elemento]=fijo
        print(f'Se ha cargado el elemento fijo: {fijo.nombre} - {fijo.direccion}')
    return serializar(myMap,"grafMap")

class mapa():
    def __init__(self,E:list,V:list) -> None:
        self.esquinas:Dict[esquina] = {}
        self.fijos:Dict[elmFijo]
        self.moviles:Dict[elmMovil]
        for vert in E:
            newVert=esquina(vert)
            self.esquinas[vert]=newVert
        for calle in V:
            ex,ey,w=re.findall("e*\d+",calle)
            if self.esquinas[ex].name==ex:
                vec=vecina(name=ey,dist=w)
                self.esquinas[ex].vecinas[ey]=vec
    def load(self,elemento):
        if type(elemento)==elmFijo:
            self.fijos[elemento.nombre]=elemento
        else:
            self.moviles[elemento.nombre]=elemento
        
class esquina():
    def __init__(self,name:str) -> None:
        self.name=name
        self.vecinas:Dict[vecina]={}
class vecina():
    def  __init__(self,name:str,dist:int) -> None:
        self.name=name
        self.distancia=dist
        self.elementos:Dict[str]={}
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
        loadElm(args["load_fix_element"])
    if args["load_movil_element"]!=None:
        print(args["load_movil_element"])
    if args["create_trip"]!=None:
        print(args["create_trip"])
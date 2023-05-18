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

def load_fix_element(element: str, direction: str):
    # Verificar si el nombre del elemento es válido
    if not element.isalnum():
        print('Error: El nombre del elemento solo puede contener caracteres alfanuméricos.')
        return
    
    # Definir el diccionario de correspondencias entre nombres y códigos
    name_mapping = {
        'H': 'hospital',
        'A': 'almacén',
        'T': 'tienda',
        'S': 'supermercado',
        'E': 'escuela',
        'K': 'kiosco',
        'I': 'iglesia'
    }
    
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
    if element in name_mapping.values():
        print(f'Error: El nombre del elemento "{element}" ya está en uso.')
        return
    
    # Crear el elemento fijo y mostrar información
    nombre = name_mapping.get(element, 'Desconocido')
    fijo = elmFijo(nombre, [dir1, dir2])
    print(f'Se ha cargado el elemento fijo: {fijo.nombre} - {fijo.direccion}')

def load_movil_element(element: str, direction: str, monto: str):
    # Verificar si el nombre del elemento es válido
    if not element.isalnum():
        print('Error: El nombre del elemento solo puede contener caracteres alfanuméricos.')
        return
    
    # Definir el diccionario de correspondencias entre nombres y códigos
    name_mapping = {
        'P': 'persona',
        'C': 'auto'
    }
    
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
    if element in name_mapping.values():
        print(f'Error: El nombre del elemento "{element}" ya está en uso.')
        return
    
    # Verificar si el monto es un valor numérico
    try:
        monto = float(monto)
    except ValueError:
        print('Error: El monto debe ser un valor numérico.')
        return
    
    # Crear el elemento móvil y mostrar información
    nombre = name_mapping.get(element, 'Desconocido')
    movil = elmMovil(nombre, [dir1, dir2], monto)
    print(f'Se ha cargado el elemento móvil: {movil.nombre} - {movil.direccion} - Monto: {movil.monto}')

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
    if args["load_fix_element"] != None:
        element, direction = args["load_fix_element"].split(',')
        load_fix_element(element.strip(), direction.strip())
    if args["load_movil_element"] != None:
        element, direction, monto = args["load_movil_element"].split(',')
        load_movil_element(element.strip(), direction.strip(), monto.strip())
    if args["create_trip"]!=None:
        print(args["create_trip"])
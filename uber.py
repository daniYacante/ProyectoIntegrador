import argparse
from typing import List
if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-create_map",help="Path al archivo mapa")
    ap.add_argument("-load_fix_element",help="Cargar elemento fijo")
    ap.add_argument("-load_movil_element",help="Cargar elemento movil")
    ap.add_argument("-create_trip",help="Crea de ser posible un viaje")
    args=vars(ap.parse_args())
    if args["create_map"]!=None:
        print(args["create_map"])
    if args["load_fix_element"]!=None:
        print(args["load_fix_element"])
    if args["load_movil_element"]!=None:
        print(args["load_movil_element"])
    if args["create_trip"]!=None:
        print(args["create_trip"])

class mapa():
    def __init__(self) -> None:
        self.esquinas:List[esquina]
        self.fijos:List[elmFijo]
        self.moviles:List[elmMovil]
class esquina():
    def __init__(self) -> None:
        self.name:str
        self.vecinas:List[vecina]
class vecina():
    def  __init__(self) -> None:
        self.name:str
        self.distancia:int
        self.elementos:List[str]
class elmFijo():
    def __init__(self,nombre,direccion) -> None:
        self.nombre=nombre
        self.direccion=direccion
class elmMovil(elmFijo):
    def __init__(self, nombre, direccion,monto) -> None:
        super().__init__(nombre, direccion)
        self.monto=monto
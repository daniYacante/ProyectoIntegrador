import argparse
from typing import Dict
import re
import pickle
"""
Pequeña función que serializa un objeto, devuelve True o False dependiendo si se pudo serializar o no
"""
def serializar(objeto,nombre):
    try:
        with open(nombre,'bw') as f:
            pickle.dump(objeto,f)
    except Exception as e:
        print(e)
        return False
    finally:
        return True
"""
Pequeña función que deserializa un objeto, devuelve el objeto o none dependiendo si se pudo deserializar o no
"""
def deserializar(nombre):
    try:
        with open(nombre,'br') as f:
            obj=pickle.load(f)
    except Exception as e:
        print(e)
        return None
    finally:
        return obj
"""
Función que se llama para crear el mapa, se lee el archivo donde esta el mapa. Al finalizar se serializa el mapa
"""
def loadMap(dir:str):
    with open(dir,'r') as mp:
        E=mp.readline().split("=")[1][1:-2].split(",")
        V=re.findall("<e\d+,e\d+,\d+>", mp.readline())
    myMap=mapa(E,V)
    # for i in range(len(myMap.esquinas)):
    #     print(myMap.esquinas[i].name)
    if serializar(myMap,"grafMap"):
        print("Map created successfully")
"""
Funcion que se llama al cargar un elemento, utilizando expresiones regulares se va a discernir entre un elemento movil
o elemento fijo segun si existe el parametro de monto al final.
"""
def loadElm(element:str):
    # Expresion regular que encuentra el objeto y las dos partes de la direccion
    patt=re.compile("([A-Z]\d+) *,*{*(<.*?>) *,*(<.*?>)}* *,*(\d+)*")
    mat=re.search(patt,element)
    elm=mat.group(1,2,3)
    myMap=deserializar("grafMap")
    if myMap==None:
        return
    # Verificar si el nombre del elemento es válido
    if not elm[0].isalnum():
        print('Error: El nombre del elemento solo puede contener caracteres alfanuméricos.')
        return
    if len(elm) != 3:
        print('Error: La dirección debe consistir en dos tuplas.')
        return
    # Crear las tuplas de dirección
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
        myMap.load(movil)
        print(f'Se ha cargado el elemento móvil: {movil.nombre} - {movil.direccion} - Monto: {movil.monto}')
    else:
        fijo = elmFijo(elm[0], [dir1, dir2])
        # Actualizar el conjunto de nombres utilizados
        myMap.load(fijo)
        print(f'Se ha cargado el elemento fijo: {fijo.nombre} - {fijo.direccion}')
    return serializar(myMap,"grafMap")
"""
Función que comprobara todo lo necesario para realizar el viaje.
Algunas de estas cosas son:
    * Que la dirección a la que se desea llegar exista.
    * Que la dirección a la que se desea llegar sea accesible desde el lugar de la persona.
    * Que la persona exista.
    * Que el auto pueda llegar a la persona.
"""
def createTrip(entrada:str):
    #De la cadena de entrada separa la persona del destino del viaje
    #El viaje puede ser un lugar fijo o una dirección particular
    argu=re.search("([A-Z]\d+)\s+(.+)",entrada)
    myMap=deserializar("grafMap")
    persona=argu.group(1)
    destino=argu.group(2)
    dest=re.search("{*(<.*?>) *,*(<.*?>)}*",destino)
    #Si el destino no es una dirección particular obtenemos la dirección del
    #elemento fijo
    if dest==None:
        if destino not in myMap.getFijos():
            if destino not in myMap.getMoviles():
                print("El destino no existe")
                return
            else:
                dest=myMap.getMoviles()[destino].getPos()
        else:
            dest=myMap.getFijos()[destino].getPos()
        dx=dest[0]
        dy=dest[1]
    else:
        dx=dest.group(1)
        dy=dest.group(2)
    #Verificamos si a donde queremos llegar esta en una calle de 2 manos
    listDest=[]
    if myMap.checkDir(dx,dy):
        listDest.append(dx)
    if myMap.checkDir(dy,dx):
        listDest.append(dy)
    #Verificamos que la direccion exista en el mapa
    if len(listDest)==0:
        print("El destino no existe")
        return 
    #Verificamos que la persona exista dentro del mapa
    if persona in myMap.getMoviles():
        print("La persona esta")
        sx,sy=myMap.getMoviles()[persona].getPos()
        saldo=myMap.getMoviles()[persona].monto
        """
        Si la calle es de una sola mano donde se encuentra la persona
        Se queda una bandera en True para cuando haya que buscar el camino desde los autos
        se tome la esquina opuesta, ya que el auto tendrá que llegar a la persona por esa
        esquina
        """
        listStart=[]
        if myMap.checkDir(sx,sy):
            listStart.append(sy)
        if myMap.checkDir(sy,sx):
            listStart.append(sx)
        SU=False
        if len(listStart)==1:
            SU=True
        """
        Se genera una lista de combinaciones de esquinas de salida y llegada, para ver cual es la que tiene menor distancia.
        Si no hay combinaciones es que no hay un camino entre la/s esquina/s de salida y la/s de llegada.
        """
        caminos=[]
        for esquinaStart in listStart:
            for esquinaDest in listDest:
                if myMap.getGroups(esquinaDest).group(1) in myMap.esquinas[myMap.getGroups(esquinaStart).group(1)].shortestPath.keys() or myMap.getGroups(esquinaStart).group(1) == myMap.getGroups(esquinaDest).group(1):
                    caminos.append((esquinaStart,esquinaDest,myMap.esquinas[myMap.getGroups(esquinaStart).group(1)].checkPath(myMap.getGroups(esquinaDest).group(1))))
        if len(caminos)==0:
            print("No hay forma de llegar al destino")
            return
        else:
            caminoMin=caminoMasCorto(myMap,caminos)
            print(f"El camino mas corto de la persona al destino es {caminoMin}")
            """
            Obtengo la lista de los autos.
            """
            listCars=[]
            for elemento in myMap.getMoviles().keys():
                if elemento[0].upper()=="C":
                    listCars.append(myMap.moviles[elemento])
            autosSeleccionados=[]
            """
            Para cada auto obtengo si se encuentra en una calle de doble mano o no, ya que como con la persona
            Cambia el como buscar a la persona
            """
            for car in listCars:
                listDirCar=[]
                dirCar=car.direccion
                if myMap.checkDir(dirCar[0],dirCar[1]):
                    listDirCar.append(dirCar[1])
                if myMap.checkDir(dirCar[1],dirCar[0]):
                    listDirCar.append(dirCar[0])
                caminosAuto=[]
                if SU:
                    listStart=[sx]
                """
                Como hicimos para ver si se podia llegar a la direccion deseada, vemos si el auto puede llegar
                a la persona.
                """
                for esquinaAuto in listDirCar:
                    for esquinaStart in listStart:
                        if myMap.getGroups(esquinaStart).group(1) in myMap.esquinas[myMap.getGroups(esquinaAuto).group(1)].shortestPath.keys() or myMap.getGroups(esquinaStart).group(1) == myMap.getGroups(esquinaAuto).group(1):
                            caminosAuto.append((esquinaAuto,esquinaStart,myMap.esquinas[myMap.getGroups(esquinaAuto).group(1)].checkPath(myMap.getGroups(esquinaStart).group(1))))
                if len(caminosAuto)==0:
                    print(f"El auto {car.nombre} no puede llegar a la persona")
                    continue
                else:
                    caminoMinAuto=caminoMasCorto(myMap,caminosAuto)
                    # print(caminoMinAuto)
                    print(f"El camino mas corto a la persona desde el auto {car.nombre} {caminoMinAuto}")
                """
                Para cada auto vamos a ver si tiene un costo menor a la de los autos anteriores.
                Si lo tiene se saca el auto de mayor costo, para insertar el nuevo auto.
                """
                precio=caminoMinAuto[2]+car.monto/4
                if saldo>=precio:
                    if len(autosSeleccionados)==0:
                        autosSeleccionados.append((car.nombre,caminoMinAuto[2],precio))
                    else:
                        EI=False
                        for i in range(len(autosSeleccionados)):
                            if caminoMinAuto[2]<autosSeleccionados[i][1]:
                                autosSeleccionados.insert(i,(car.nombre,caminoMinAuto[2],precio))
                                EI=True
                                break
                        if not EI:
                            autosSeleccionados.append((car.nombre,caminoMinAuto[2],precio))
                        if len(autosSeleccionados)>3:
                            autosSeleccionados.pop()
            if len(autosSeleccionados)==0:
                print("No hay autos disponibles para realizar el viaje")
                return
            print("Autos disponibles para realizar el viaje:")
            for i in range(len(autosSeleccionados)):
                print(i+1," -",autosSeleccionados[i][0],"precio: ",autosSeleccionados[i][2])  
            """
            Si se elige un auto para realizar el viaje se procede a actualizar las direcciones tanto del auto
            como de la persona como asi descontar el costo del viaje a la persona.
            """
            seleccion=input("Ingrese el numero de la opción que va a elegir\nIngrese 'exit' para cancelar\n")
            if seleccion=="exit":
                return
            else:
                myMap.getMoviles()[persona].monto-=autosSeleccionados[int(seleccion)-1][2]
                myMap.getMoviles()[persona].direccion=[dx,dy]
                myMap.getMoviles()[autosSeleccionados[int(seleccion)-1][0]].direccion=[dx,dy]
            print("Viaje realizado")
            print(f"Dirección de la persona: {persona}",myMap.getMoviles()[persona].getPos())
            print(f"Saldo de la persona: {persona}",myMap.getMoviles()[persona].getMonto())
            print(f"Dirección del auto: {myMap.getMoviles()[autosSeleccionados[int(seleccion)-1][0]].nombre}",myMap.getMoviles()[autosSeleccionados[int(seleccion)-1][0]].getPos())
            return serializar(myMap,"grafMap")
    else:
        print("La persona no existe")
        return
def caminoMasCorto(myMap,caminos):
    # print(caminos)
    distMin=-1
    caminoMin=()
    for camino in caminos:
        distancia=float(myMap.getGroups(camino[0]).group(2))+float(myMap.getGroups(camino[1]).group(2))+float(camino[2][0])
        if distancia<distMin or distMin==-1:
            distMin=distancia
            intermedios=[n for n in reversed(camino[2][1])]
            if myMap.getGroups(camino[0]).group(1)!=myMap.getGroups(camino[1]).group(1):
                intermedios.insert(0,myMap.getGroups(camino[0]).group(1))
                intermedios.append(myMap.getGroups(camino[1]).group(1))
            caminoMin=(camino[0],camino[1],distMin,intermedios)
    return caminoMin
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
                    if w<self.esquinas[ex].shortestPath[ey][0]:
                        self.esquinas[ex].shortestPath[ey]=[w,[]]
                else:
                    self.esquinas[ex].shortestPath[ey]=[w,[]]
                tablaEy=self.esquinas[ey].shortestPath
                for nodo in tablaEy.keys():
                    if nodo!=ex:
                        lista=tablaEy[nodo][1].copy()
                        newList=lista.append(ey)
                        if nodo in self.esquinas[ex].shortestPath.keys():
                            if self.esquinas[ex].shortestPath[nodo][0]>tablaEy[nodo][0]+w:
                                self.esquinas[ex].shortestPath[nodo]=[tablaEy[nodo][0]+w,lista]
                        else:
                            self.esquinas[ex].shortestPath[nodo]=[tablaEy[nodo][0]+w,lista]
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
        #shortestPath:{esquina}=[w,[camino de esquinas]]
        self.shortestPath={}
    def checkPath(self,nodo):
        if nodo==self.name:
            return [0,[self.name]]
        else:
            return self.shortestPath[nodo]
    def updateDist(self,tabla:dict,esquinas:dict,hijo):
        d=self.vecinas[hijo].distancia
        NHC=True
        for nodo in tabla.keys():
            if nodo!=self.name:
                lista=tabla[nodo][1].copy()
                newList=lista.append(hijo)
                if nodo in self.shortestPath.keys():
                    if self.shortestPath[nodo][0]>tabla[nodo][0]+d:
                        self.shortestPath[nodo]=[tabla[nodo][0]+d,lista]
                        NHC=False
                else:
                    self.shortestPath[nodo]=[tabla[nodo][0]+d,lista]
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
    def getMonto(self):
        return self.monto

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
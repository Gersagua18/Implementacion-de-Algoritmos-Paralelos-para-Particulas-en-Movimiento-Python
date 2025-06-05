import threading
import multiprocessing
from collections import Counter
import time
frecuencia_sucuencial=Counter()
bloqueo=threading.Lock()
resultado_s=[]
elementos=100000
''' Paralelo'''
def busqueda_posicion_paralela(buscar, inicio, fin,resultado_p):
    with open("pasos.txt","r") as archivo:
        for indice,linea in enumerate(archivo):
            if inicio<=indice<fin:
                bloques=linea.strip().split(' ')
                for bloque in bloques:
                    valor=bloque.strip().split(',')
                    x=round(float(valor[0]),2)
                    y=round(float(valor[1]),2)
                    w=round(float(buscar[0]),2)
                    z=round(float(buscar[1]),2)
                    if x==w and y==z:
                        with bloqueo:
                            resultado_p.append({"linea":indice, "x": valor[0], "y": valor[1]})
            if indice>fin:
                break
def mejores_cinco_paralela(inicio,fin,frecuencia_paralela):
    with open("pasos.txt","r") as archivo:
        for indice,linea in enumerate(archivo):
            if inicio<=indice<fin:
                bloques=linea.strip().split(' ')
                for bloque in bloques:
                    valor=bloque.strip().split(',')
                    x=round(float(valor[0]),2)
                    y=round(float(valor[1]),2)
                    with bloqueo:
                        frecuencia_paralela[(x,y)]=frecuencia_paralela.get((x,y),0)+1
            if indice>fin:
                break
'''Secuencial'''
def busqueda_posicion_secuencial(buscar):
    with open("pasos.txt","r") as archivo:
        for indice,linea in enumerate(archivo):
            bloques=linea.strip().split(' ')
            for bloque in bloques:
                valor=bloque.strip().split(',')
                x=round(float(valor[0]),2)
                y=round(float(valor[1]),2)
                w=round(float(buscar[0]),2)
                z=round(float(buscar[1]),2)
                if x==w and y==z:
                    resultado_s.append({"linea": indice,"x": valor[0],"y":valor[1]})
def mejores_cinco_secuencial():
    with open("pasos.txt","r") as archivo:
        for linea in archivo:
            bloques=linea.strip().split(' ')
            for bloque in bloques:
                valor=bloque.strip().split(',')
                x=round(float(valor[0]), 2)
                y=round(float(valor[1]), 2)
                frecuencia_sucuencial[(x, y)]+=1
def principal():
    buscar=[]
    #buscar.append(60.3051)
    #buscar.append(374.9899)
    buscar.append(float(input("Ingrese el valor de posicion X: ")))
    buscar.append(float(input("Ingrese el valor de posicion Y: ")))
    num_procesos=4
    elem_hilo=elementos//num_procesos
    procesos=[]
    manager=multiprocessing.Manager()
    frecuencia_paralelo=manager.dict()
    resultado_p=manager.list()
    inicio_paralelo=time.time()
    for proceso_actual in range(num_procesos):
        inicio=proceso_actual*elem_hilo
        fin=(proceso_actual+1)*elem_hilo
        p1=multiprocessing.Process(target=busqueda_posicion_paralela,args=(buscar, inicio,fin,resultado_p))
        p2=multiprocessing.Process(target=mejores_cinco_paralela,args=(inicio,fin,frecuencia_paralelo))
        procesos.append(p1)
        procesos.append(p2)
        p1.start()
        p2.start()
    fin_paralelo=time.time()
    for h in procesos:
           h.join()
    inicio_secuencial=time.time()
    busqueda_posicion_secuencial(buscar)
    mejores_cinco_secuencial()
    fin_secuencial=time.time()
    return (fin_paralelo-inicio_paralelo),(fin_secuencial-inicio_secuencial),resultado_p,frecuencia_paralelo
if __name__=="__main__":
    tiempo_paralelo,tiempo_secuencial,resultado_p,frecuencia_paralelo=principal()
    print("Tiempo de ejecucion paralelo: ",tiempo_paralelo)
    print("busqueda paralela: ",resultado_p)
    print("Top 5 coordenadas más repetidas paralela:")
    for coord, veces in Counter(frecuencia_paralelo).most_common(10):
        print(f"Coordenada {coord} se repite {veces} veces.")
    print("="*30)
    print("Tiempo de ejecucion secuencial: ",tiempo_secuencial)
    print("Busqueda secuencial: ",resultado_s)
    print("Top 5 coordenadas más repetidas secuencial:")
    for coord, veces in frecuencia_sucuencial.most_common(10):
        print(f"Coordenada {coord} se repite {veces} veces.")
    print("="*30)
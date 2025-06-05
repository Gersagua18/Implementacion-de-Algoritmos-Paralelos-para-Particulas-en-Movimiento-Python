import threading
import multiprocessing
from collections import Counter
import time
frecuencia_sucuencial=Counter()
bloqueo=threading.Lock()
resultado_s=[]
elementos=100000
def tiempo_busqueda(buscar,inicio,fin,resultado_p,tiempos,i):
    inicio_tiempo=time.time()
    busqueda_posicion_paralela(buscar,inicio,fin,resultado_p)
    fin_tiempo=time.time()
    tiempos[i]=fin_tiempo-inicio_tiempo
def tiempo_mejores(inicio,fin,frecuencia_paralela,tiempos,i):
    inicio_tiempo=time.time()
    mejores_diez_paralela(inicio,fin,frecuencia_paralela)
    fin_tiempo=time.time()
    tiempos[i]=fin_tiempo-inicio_tiempo
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
def mejores_diez_paralela(inicio,fin,frecuencia_paralela):
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
def mejores_diez_secuencial():
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
    tiempos_busqueda=manager.list([0]*num_procesos)
    tiempos_mejores=manager.list([0]*num_procesos)
    for proceso_actual in range(num_procesos):
        inicio=proceso_actual*elem_hilo
        fin=(proceso_actual+1)*elem_hilo
        p1=multiprocessing.Process(target=tiempo_busqueda,args=(buscar, inicio,fin,resultado_p,tiempos_busqueda,proceso_actual))
        p2=multiprocessing.Process(target=tiempo_mejores,args=(inicio,fin,frecuencia_paralelo,tiempos_mejores,proceso_actual))
        procesos.append(p1)
        procesos.append(p2)
    inicio_paralelo=time.time()
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    fin_paralelo = time.time()
    inicio_secuencial_buscar=time.time()
    busqueda_posicion_secuencial(buscar)
    fin_secuencial_buscar=time.time()
    inicio_secuencial_mejores=time.time()
    mejores_diez_secuencial()
    fin_secuencial_mejores=time.time()
    resultados=[]
    resultados.append(fin_secuencial_buscar-inicio_secuencial_buscar)
    resultados.append(fin_secuencial_mejores-inicio_secuencial_mejores)
    resultados.append(tiempos_busqueda)
    resultados.append(tiempos_mejores)
    return (fin_paralelo-inicio_paralelo),resultados,resultado_p,frecuencia_paralelo
if __name__=="__main__":
    tiempo_paralelo,resultados,resultado_p,frecuencia_paralelo=principal()
    print("Tiempo de ejecucion total paralelo: ",tiempo_paralelo)
    print("busqueda paralela: ",resultado_p)
    print("Tiempo busqueda paralelo: ",resultados[2])
    print("Top 5 coordenadas más repetidas paralela:")
    for coord, veces in Counter(frecuencia_paralelo).most_common(10):
        print(f"Coordenada {coord} se repite {veces} veces.")
    print("Tiempo mejores 10 paralelo: ",resultados[3])
    print("="*30)
    print("Tiempo de ejecucion secuencial: ",resultados[0]+resultados[1])
    print("Busqueda secuencial: ",resultado_s)
    print("Tiempo busqueda secuencial: ",resultados[0])
    print("Top 5 coordenadas más repetidas secuencial:")
    for coord, veces in frecuencia_sucuencial.most_common(10):
        print(f"Coordenada {coord} se repite {veces} veces.")
    print("Tiempo mejores 10 secuencial: ",resultados[1])
    print("="*30)
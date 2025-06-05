import threading
import random
import time
import os
cant_elem=1000000
pasos=100
tiempo=1.0
bloqueo=threading.Lock()
def escribir_mover(inicio,fin,hilo_actual):
    txt_temporal=f"temporal_hilo_{hilo_actual}.txt"
    with open(txt_temporal,"w") as archivo:
        for i in range(inicio,fin):
            x=random.uniform(0,1000)
            y=random.uniform(0,1000)
            vx=random.uniform(0,10)
            vy=random.uniform(0,10)
            with bloqueo:
                archivo.write(f"{x:.4f},{y:.4f}")
            for paso in range(pasos):
                x+=vx*tiempo
                y+=vy*tiempo
                with bloqueo:
                    archivo.write(f" {x:.4f},{y:.4f}")
            with bloqueo:
                    archivo.write("\n")
def principal():
    num_hilos=4
    elem_hilo=cant_elem//num_hilos
    tiempo_inicio=time.time()
    hilos=[]
    inicio=0
    for i in range(num_hilos):
        fin=inicio+elem_hilo
        h=threading.Thread(target=escribir_mover,args=(inicio,fin,i))
        hilos.append(h)
        h.start()
        inicio=fin
    for h in hilos:
        h.join()
    with open("pasos.txt","w") as txt_final:
        for i in range(num_hilos):
            t_eliminar=f"temporal_hilo_{i}.txt"
            with open(t_eliminar,"r") as temporal:
                txt_final.write(temporal.read())
            os.remove(t_eliminar)
    tiempo_fin=time.time()
    print("tiempo: ",tiempo_fin-tiempo_inicio)
if __name__=="__main__":
    principal()
    print("="*30) 
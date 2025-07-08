import json #impore json 
import os

#cargar el ranking desde json
def cargar_ranking(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            return json.load(archivo) #es para leer datos y convertirlos en lista
    except FileNotFoundError:
        return [] #si no existe retorna lista vacia 
    
#el guardado del ranking en json
def guardar_ranking(nombre_archivo, ranking):
    with open(nombre_archivo, 'w') as archivo: 
        json.dump(ranking, archivo, indent=4) #ordena 

#agregar un puntaje si corresponde
def actualizar_ranking(nombre_archivo, nombre_jugador, nuevo_puntaje):
    ranking = cargar_ranking(nombre_archivo)
    ranking = [j for j in ranking if j["nombre"] != nombre_jugador]
    #agrega nuevo puntaje
    ranking.append({"nombre": nombre_jugador, "puntaje": nuevo_puntaje})
    #ordenar de menor a mayor 
    ranking = sorted(ranking, key=lambda x: x["puntaje"], reverse=True) #sorte ordena listas, key indica por que ordenar y reverse=true ordena de menor a mayor
    
    #solo guarda los 5 mejores
    ranking = ranking[:5] #se queda con los mejores 5 puntajes
    guardar_ranking(nombre_archivo, ranking)

#mostrar los rankings
def mostrar_ranking(nombre_archivo):
    ranking = cargar_ranking(nombre_archivo)
    return [(j["nombre"], j["puntaje"]) for j in ranking]




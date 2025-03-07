import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
tablero_tamanio = 50 #DEfinimos el tamaño del tablero
tablero = [] #tablero es una lista vacia de tablero_tamanio²
for i in range(tablero_tamanio):
    row = [] #Row es una lista vacia
    for j in range(tablero_tamanio*2):
        row.append(0) #Agregamos un cero a la lista row
    tablero.append(row) #Agregamos la lista row a la lista tablero
tablero[0][len(tablero[0]) // 2] = 1
tablero_np = np.array(tablero) #Convertimos la lista tablero en un array de numpy
#Listo arranquemos con el juego
for i, fila in tqdm(enumerate(tablero), total=len(tablero), desc="Calculando..."): #Iteramos sobre las filas del tablero
    if i > 0:
        for j, celda in enumerate(fila):
            if j == 0: #Si estamos en la primera columna asumimos que la celda de la izquierda es 0
                izq = 0
                cen = tablero[i-1][j]
                der = tablero[i-1][j+1]
            elif j == len(fila)-1: #Si estamos en la ultima columna asumimos que la celda de la derecha es 0
                der = 0
                cen = tablero[i-1][j]
                izq = tablero[i-1][j-1]
            else: # Si no estamos en los extremos, tomamos los valores de las celdas de la fila anterior
                izq = tablero[i-1][j-1]
                cen = tablero[i-1][j]
                der = tablero[i-1][j+1]
            #Ahora vamos a definir la regla 90, ya tenemos centro izquierda y derecha, apliquemos la regla
            #000->0, 001->1, 010->0, 011->1, 100->1, 101->0, 110->1, 111->0

            #000->0
            if izq == 0 and cen == 0 and der == 0:
                tablero[i][j] = 0 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #001->1
            if izq == 0 and cen == 0 and der == 1:
                tablero[i][j] = 1 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #010->0
            if izq == 0 and cen == 1 and der == 0:
                tablero[i][j] = 0 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #011->1
            if izq == 0 and cen == 1 and der == 1:
                tablero[i][j] = 1 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #100->1
            if izq == 1 and cen == 0 and der == 0:
                tablero[i][j] = 1 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #101->0
            if izq == 1 and cen == 0 and der == 1:
                tablero[i][j] = 0 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #110->1
            if izq == 1 and cen == 1 and der == 0:
                tablero[i][j] = 1 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
            #111->0
            if izq == 1 and cen == 1 and der == 1:
                tablero[i][j] = 0 # En caso de querer aplicar otra regla, cambiar el 0 por el valor deseado
print('-'*50) #Imprimimos una linea para separar
tablero_np = np.array(tablero) #Convertimos la lista tablero en un array de numpy

plt.figure(figsize=(10,10))
plt.imshow(tablero_np, cmap='gray_r')
plt.title("Tablero Regla 90", fontsize=20)
plt.axis('off')  # Ocultar ejes
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 19:22:23 2022
Modified on Tue Mar 6 18:31:11 2025
Conway's Game of Life en Python 3.12 con PyGame
@author: JulianCastillo

    Created By
    -------
    Julian Andres Castillo
        DESCRIPTION. Ingeniero de Sistemas M.Sc. En Ingeniería, creado para el 
        curso de Simulación Basada en agentes de posgrados UdeA.
        Adaptado y mejorado para el tutorial de Simulacion Basada en Agentes de ASOCIO 20250311
        Basado en el concepto de https://www.neuralnine.com/
"""

import time
import pygame
import numpy as np
#Colores del juego en RGB
color_fondo = (10, 10, 10) #Color del fondo (Casi Negro)
color_malla = (40, 40, 40) #Color de la malla (Casi negro pero visible)
color_celda_muerta = (170, 170, 170) #Color de celda muerta gris
color_celda_viva = (255,255,255) #Color de celda viva blanco

def MatrizProbabilidad(row,col,probabilidad):
    """
    Genera una matriz de tamaño (row, col) con valores 0 y 1, donde la probabilidad
    de que un elemento sea 0 es 'probabilidad' y la probabilidad de que sea 1 es '1 - probabilidad'.

    Parámetros:
    row (int): Número de filas de la matriz.
    col (int): Número de columnas de la matriz.
    probabilidad (float): Probabilidad de que un elemento de la matriz sea 0.

    Retorna:
    numpy.ndarray: Matriz de tamaño (row, col) con valores 0 y 1.
    """
    return np.random.choice([0, 1], size=(row,col), p=[probabilidad, 1-probabilidad])
    #                      opciones     tamaño            probabildiades de 0 y 1
def ReglasGameOfLife(screen, cells, size, estado_ejecucion=False): 
    """
    Aplica las reglas del juego de la vida de Conway a la matriz de celdas y actualiza la pantalla.

    Parámetros:
    screen (pygame.Surface): La superficie de PyGame donde se dibujan las celdas.
    cells (numpy.ndarray): La matriz actual de celdas, donde 1 representa una celda viva y 0 una celda muerta.
    size (int): El tamaño de cada celda en píxeles.
    estado_ejecucion (bool): Indica si el juego está en ejecución para actualizar los colores de las celdas.

    Retorna:
    numpy.ndarray: La matriz actualizada de celdas después de aplicar las reglas del juego de la vida.
    """
    celdas_actualizadas = np.zeros((cells.shape[0], cells.shape[1])) #Creamos una matriz de ceros para tener las celdas actualizadas
    for row, col in np.ndindex(cells.shape): # Iteraremos sobre todos los elementos
        cont_cvivas = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col] #USando el vecindario Moore contamos las celdas vivas
        #Row y Col mas dos, los limites del slicing son [inicio:final] y el final no se incluye
        cell_color = cells[row, col]
        if cell_color == 0: # Con su valor se asigna el color a la celda
            color = color_fondo
        else:
            color = color_celda_viva
        if cells[row, col] == 1: #Si la celda esta viva debemos preguntar las reglas
            if cont_cvivas < 2 or cont_cvivas > 3: #Si la celda tiene menos de dos o mas de tres vecinos vivos muere
                celdas_actualizadas[row,col] = 0
                if estado_ejecucion:
                    color = color_celda_muerta
            elif 2 <= cont_cvivas <= 3: #Si la celda tiene dos o tres vecinos vivos sobrevive
                celdas_actualizadas[row,col] = 1
                if estado_ejecucion:
                    color = color_celda_viva
        else:
            if cont_cvivas == 3:#Si la celda tiene exactamente tres vecinos vivos nace
                celdas_actualizadas[row,col] = 1
                if estado_ejecucion:
                    color = color_celda_viva
        pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1)) #Usando Draw y rect para pintar un rectangulo con pygame
    return celdas_actualizadas

def EstadoJuego(tamanio_malla, tamanio_celda, velocidad): #Funcion para imprimir el estado inicial del juego y sus valores
    """
    Imprime el estado inicial del juego.

    Parámetros:
    tamanio_malla (tuple): Tamaño de la ventana en pixeles (ancho, alto).
    tamanio_celda (tuple): Tamaño de la malla en celdas (filas, columnas).
    velocidad (float): Velocidad de refrescado de la pantalla.
    """
    print('Estado inicial del juego:')
    print('\tTamaño de la ventana=', (tamanio_malla[1], tamanio_malla[0]), ' Valores en Pixeles')
    print('\tTamaño de la malla=', tamanio_celda)
    print('\tVelocidad de refrescado=', velocidad)
    
def main(p, malla): #Funcion principal del juego
    """
    Función principal que ejecuta el juego de la vida de Conway utilizando PyGame.

    Inicializa PyGame, configura la pantalla y las celdas, y ejecuta el bucle principal del juego.
    Permite iniciar, detener y ajustar la velocidad del juego mediante eventos de teclado y mouse.
    """
    pygame.init()
    tamanio_celdas = (50,50) #Tamaño inicial de la malla, Se puede cambiar.
    if p == 0:
        #Creamos una malla de celdas en cero de tamaño shape[0]xshape[1] (mxn)
        cells = np.zeros(tamanio_celdas)

    elif p == 1:
        cargatxt = np.loadtxt(malla, dtype=int)
        cells = cargatxt
    else: #La probabilidad es diferente de cero por lo tanto debemos detallar la malla con dicho valor p
        cells = MatrizProbabilidad(tamanio_celdas[0], tamanio_celdas[1], p)
        
    tamanio_celdas = (cells.shape[0], cells.shape[1])
    tamanio_malla = (cells.shape[0]*10,cells.shape[1]*10)
    pygame.display.set_caption("Conway's Game of Life, Malla de " + str(tamanio_celdas) + " | Presiona Barra espaciadora para iniciar o detener.")
    screen = pygame.display.set_mode((tamanio_malla[1], tamanio_malla[0])) #Las matrices son filas por columnas, las pantallas son columnas por filas, se debe invertir el valor
    #cells = np.zeros(tamanio_celdas)
    screen.fill(color_malla)
    ReglasGameOfLife(screen, cells, 10)
    pygame.display.flip()
    pygame.display.update()
    velocidad = 0.0001 #La velocidad detalla la velocidad de refrescado de la pantalla
    running = False
    EstadoJuego(tamanio_malla, tamanio_celdas, velocidad)
    while True:
        #Variables generales para la evolucion del juego

        for event in pygame.event.get(): #si el usuario cierra la ventana de juego se cierra el juego
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN: #Control de evento si el usuario presiona teclas
                if event.key == pygame.K_SPACE:#Control para la barra espaciadora, activar o desactivar el juego
                    running = not running
                    ReglasGameOfLife(screen, cells, 10)
                    pygame.display.update()
            if event.type == pygame.KEYDOWN: #Control para otras teclas.
                if event.key == pygame.K_UP: #Control para aumentar la velocidad
                    print('Velocidad anterior=', velocidad)
                    velocidad = velocidad / 10
                    print('Velocidad actual=', velocidad)
                    EstadoJuego(tamanio_malla, cells.size, velocidad)
                elif event.key == pygame.K_DOWN: #Control para disminuir la velocidad
                    print('Velocidad anterior=', velocidad)
                    velocidad = velocidad * 10
                    print('Velocidad actual=', velocidad)
                    EstadoJuego(tamanio_malla, cells.size, velocidad)
            if pygame.mouse.get_pressed()[0]: #Control para el mouse, si se presiona el boton izquierdo se pinta la celda
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                ReglasGameOfLife(screen,cells, 10)
                pygame.display.update()
                
        screen.fill(color_malla) #Se llena la pantalla con el color de la malla
        if running: #Mostrar el estado del juego
            cells = ReglasGameOfLife(screen, cells, 10, estado_ejecucion=True)
            pygame.display.update()
        
        time.sleep(velocidad) #Control de velocidad del juego

if __name__ == '__main__': #Menu de opciones para el usuario
    print('Ejecutando el juego de la vida de Conway en Python 3 con PyGame')
    print('Seleccione el tipo de malla a utilizar:')
    print('\t0. Malla vacía, con clic sostenido se pintan las celdas')
    print('\t1. Cargar un documento txt, Seleccionar esta opción Mostrará las opciones disponibles')
    print('\t2. Crear una malla con una probabilidad p de celdas vivas, Seleccionar esta opción pedira un valor p entre cero y uno')
    try:
        p = int(input('Ingresar la opción deseada [0,1,2]: '))
        malla = ''
        if p in [0,1,2]:
            print('Opción seleccionada:', p)
            if p == 0:
                prob = 0
                print('Malla vacía, con clic sostenido se pintan las celdas')
                print('El juego inicia con barra espaciadora')
            elif p == 1:
                prob = 1
                print('Cargar un documento txt, a continuación las opciones disponibles:')
                print('A --> Cargar el archivo GoL_GameOfLife.txt')
                print('B --> Cargar el archivo GoL_Engine_Cordership.txt')
                print('C --> Cargar el archivo GoL_EngineCordershipEater.txt')
                print('D --> Cargar el archivo GoL_PufferfiShrake.txt')
                p = input('Ingresar la opción deseada [A, B, C, D]: ').upper()
                if p in ['A','B','C','D']:
                    print('Opción seleccionada:', p)
                    match p:
                        case 'A':
                            print('Cargando el archivo GoL_GameOfLife.txt')
                            malla = 'GoL_GameOfLife.txt'
                        case 'B':
                            print('Cargando el archivo GoL_Engine_Cordership.txt')
                            malla = 'GoL_Engine_Cordership.txt'
                        case 'C':
                            print('Cargando el archivo GoL_EngineCordershipEater.txt')
                            malla = 'GoL_EngineCordershipEater.txt'
                        case 'D':
                            print('Cargando el archivo GoL_PufferfiShrake.txt')
                            malla = 'GoL_PufferfiShrake.txt'         
                else:
                    raise ValueError('Opción no válida')
            else:
                print('Crear una malla con una probabilidad p de celdas vivas')
                prob = float(input('Ingresar un valor p entre cero y uno: '))
                if 0 <= p and p <= 1:
                    print('Probabilidad seleccionada:', prob)
                else:
                    raise ValueError('Valor p no válido')
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    main(prob, malla)
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pygame
import numpy as np
import time

pygame.init()

# Creació de la pantalla
width, height = 700, 700
screen = pygame.display.set_mode((height, width))

# Pintar el fons de color fosc
green = (0, 255, 0)
bg = 25, 25, 25
screen.fill(bg)

# Quantes celules volem a cada eix
nxC, nyC = 50, 50

# Dimension de les celules
dimCW = width / nxC
dimCH = height / nyC

# Estat de les celules. Vives = 1; Mortes = 0
gameState = np.zeros((nxC, nyC))


# Inicialitzacio d'un automata en moviment
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1



# Activar pausa (per defecte activat per veure la forma inicial de l'automata)
pauseExec = True

# Controla la finalització del joc:
endGame = False

# Bucle d'execució
while not endGame:

    newGameState = np.copy(gameState)
    screen.fill(bg) # tornar a pintar per evitar superposició

    time.sleep(0.1) # descans entre iteracions

    # Pausa i ratolí
    ev = pygame.event.get()

    for event in ev:

        # Si tanquen la pestanya s'acaba el joc
        if event.type == pygame.QUIT:
            endGame = True

        # Si premen qualsevol tecla es pausa / repren el joc
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        # Detecció del click del ratolí per activar / desactivar celules
        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            # coordenades del mouse
            posX, posY = pygame.mouse.get_pos()
            # de coordenades a pixels
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            # permutar entre vida i mort
            newGameState[celX, celY] = not gameState[celX, celY]


    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                # Veins a prop
                n_neigh =   gameState[(x-1) % nxC , (y-1) % nyC] + \
                            gameState[(x)   % nxC , (y-1) % nyC] + \
                            gameState[(x+1) % nxC , (y-1) % nyC] + \
                            gameState[(x-1) % nxC , (y)   % nyC] + \
                            gameState[(x+1) % nxC , (y)   % nyC] + \
                            gameState[(x-1) % nxC , (y+1) % nyC] + \
                            gameState[(x)   % nxC , (y+1) % nyC] + \
                            gameState[(x+1) % nxC , (y+1) % nyC]

                # Norma 1: una celula morta amb 3 veines vives, reviu
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1

                # Norma 2: una celula viva amb menys de 2 o més de 3 veines vives, es mor
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0

                # Polygon de cada celula al dibuixar
                poly = [((x)     * dimCW, y * dimCH), # a baix a esquerra
                        ((x+1)   * dimCW, y * dimCH), # a baix a dreta
                        ((x+1)   * dimCW, (y+1) * dimCH), # a dalt a dreta
                        ((x)     * dimCW, (y+1) * dimCH)] # a dalt a esquerra

                # Dibuixem la celula
                if newGameState[x,y] == 0:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                else:
                    if pauseExec:
                        pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
                    else:
                        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualització
    gameState = np.copy(newGameState) # actualitzar l'estat del joc
    pygame.display.flip() # actualitzar la pantalla

import pygame
import numpy as np
import time

pygame.init()

# Width and height of screen
width, height = 600, 600
# Creating the game
screen = pygame.display.set_mode((height, width))
# Set background screen to black
bg = 25, 25, 25
screen.fill(bg)

# Number of cells
nxC, nyC = 50, 50
# Dimensions of cells
dimCW = width / nxC
dimCH = height / nyC

# State of cells. Lives = 1; Deads = 0;
gameState = np.zeros((nxC, nyC))

# Static automaton
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Movil automaton
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Execution control
pauseExcet = False

# Execution loop
while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Catching mouse and keyboard events
    ev = pygame.event.get()

    for event in ev:
        # Detect if a key was pressed
        if event.type == pygame.KEYDOWN:
            pauseExcet = not pauseExcet

        # Detect if mouse was pressed
        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]


    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExcet:
                # Calculate number of near neighbors
                n_neight =  gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x) % nxC, (y - 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                            gameState[(x - 1) % nxC, (y) % nyC] + \
                            gameState[(x + 1) % nxC, (y) % nyC] + \
                            gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                            gameState[(x) % nxC, (y + 1) % nyC] + \
                            gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule 1: If a dead cell has 3 live neighbors, will relife
                if gameState[x, y] == 0 and n_neight == 3:
                    newGameState[x, y] = 1

                # Rule 2: If a life cell has less than 2 or more than 3 live neighbors, will dead
                elif gameState[x, y] == 1 and (n_neight < 2 or n_neight > 3):
                    newGameState[x, y] = 0

            # Creating polygon of each cell to draw
            poly = [
                ((x) * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH)
            ]

            # Drawing cell for each couple of x and y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Updating new game state
    gameState = np.copy(newGameState)
    pygame.display.flip()

import random
import sys
import pygame

from itertools import cycle
from pygame.locals import *

#Set display Parameters
FPS = 60
SCREENHEIGHT = 1300
SCREENWIDTH = 700
PIPEGAPSIZE = 150
BASEY = SCREENHEIGHT * 0.79

#Dictionary for Game assets
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

#List of all sprites
PLAYERS_LIST = ()
BACKGROUND_LIST = ('SRC/assets/day.png', 'SRC/assets/night.png')
PIPES_LIST = ()

#Kizar
def main():
    global SCREEN,FPSCLOCK
    pygame.init()
    
    #add counter images
    IMAGES['numbers'] = ('...')
    #add gameover image
    IMAGES['gameover'] = pygame.image.load('...').convert_alpha()
    #add ground image
    IMAGES['base'] = pygame.image.load('...').convert_alpha()
    
    
    #Sounds implement
    
    # sounds
    #if 'win' in sys.platform:
    #soundExt = '.wav'
    #else:
    #soundExt = '.ogg'
    
    # SOUNDS['die']    = pygame.mixer.Sound('...' + soundExt)
    # SOUNDS['hit']    = pygame.mixer.Sound('...' + soundExt)
    # SOUNDS['point']  = pygame.mixer.Sound('...' + soundExt)
    # SOUNDS['swoosh'] = pygame.mixer.Sound('...' + soundExt)
    # SOUNDS['wing']   = pygame.mixer.Sound('...' + soundExt)


    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)
    


#Rushi
def showWelcomeAnimation():


#Sunny
def mainGame(movementInfo):

#Rushi
def showGameOverScreen(crashInfo):

#Kizar
def showScore(score):
    scoreDigi = []
    numWidth = 0

    for x in list(str(score)):

        scoreDigi.append(int(x))

    for digit in scoreDigi:
        numWidth += IMAGES['numbers'][digit].get_width()


    offSetX = (SCREENWIDTH - numWidth) /  2

    for digit in scoreDigi:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        offSetX += IMAGES['numbers'][digit].get_width()
    

#Sunny
def playerShm(playerShm):

#Rushi
def getRandomPipe():

#Kizar
def checkCrash(player, upperPipes, lowerPipes):
    #Return True if collition
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

#Kizar
def pixelCollision(rect1, rect2, hitmask1, hitmask2):

    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

#Sunny
def getHitmask(image):

if __name__ == '__main__':
    main()

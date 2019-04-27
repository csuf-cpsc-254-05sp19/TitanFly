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
BACKGROUND_LIST = ()
PIPES_LIST = ()


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
        randBg = random.randint(0, len(BACKGROUND_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUND_LIST[randBg]).convert()
        
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


def showWelcomeAnimation():



def mainGame(movementInfo):


def showGameOverScreen(crashInfo):


def playerShm(playerShm):


def getRandomPipe():

def checkCrash(player, upperPipes, lowerPipes):

def pixelCollision(rect1, rect2, hitmask1, hitmask2):

def getHitmask(image):

if __name__ == '__main__':
    main()

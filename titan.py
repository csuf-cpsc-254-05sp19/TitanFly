import random
import sys
import pygame

from itertools import cycle
from pygame.locals import *

#Set display Parameters
FPS = 60
SCREENHEIGHT = 1135
SCREENWIDTH = 700
PIPEGAPSIZE = 150
BASEY = SCREENHEIGHT * 0.9

#Dictionary for Game assets
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

#List of all sprites
PLAYERS_LIST = ('SRC/assets/birdup.png','SRC/assets/bird.png','SRC/assets/birddown.png')
BACKGROUND_LIST = ('SRC/assets/day.png', 'SRC/assets/night.png')
PIPES_LIST = ('SRC/assets/pipe-green.png','SRC/assets/pipe-red.png')

#try:
#    xrange
#except NameError:
#    xrange = range

#Kizar
def main():
    global SCREEN,FPSCLOCK
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Titan Fly')

    #add counter images
    IMAGES['numbers'] = (
        pygame.image.load('SRC/assets/1.png').convert_alpha(),
        pygame.image.load('SRC/assets/2.png').convert_alpha(),
        pygame.image.load('SRC/assets/3.png').convert_alpha(),
        pygame.image.load('SRC/assets/epp.png').convert_alpha(),
        pygame.image.load('SRC/assets/4.png').convert_alpha(),
        pygame.image.load('SRC/assets/5.png').convert_alpha(),
        pygame.image.load('SRC/assets/6.png').convert_alpha(),
        pygame.image.load('SRC/assets/7.png').convert_alpha(),
        pygame.image.load('SRC/assets/8.png').convert_alpha(),
        pygame.image.load('SRC/assets/9.png').convert_alpha(),
        pygame.image.load('SRC/assets/10.png').convert_alpha(),
        pygame.image.load('SRC/assets/12.png').convert_alpha(),
        pygame.image.load('SRC/assets/13.png').convert_alpha(),
        pygame.image.load('SRC/assets/14.png').convert_alpha(),
        pygame.image.load('SRC/assets/15.png').convert_alpha(),
        pygame.image.load('SRC/assets/16.png').convert_alpha()
        )
    #add gameover image
    IMAGES['gameover'] = pygame.image.load('SRC/assets/gameover.png').convert_alpha()
    #welcome image
    IMAGES['message'] = pygame.image.load('SRC/assets/message.png').convert_alpha()
    #add ground image
    IMAGES['base'] = pygame.image.load('SRC/assets/base.png').convert_alpha()



    #Sounds implement
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('SRC/assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('SRC/assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('SRC/assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('SRC/assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('SRC/assets/audio/wing' + soundExt)


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
    """This function shows the welcome animation at the beginning of the game"""

    # Index of the player blitting on the SCREEN
    playerIndex = 0

    # Player index generator to switch between the three different characters provided
    playerIndexGenerator = cycle([0, 1, 2, 1])

    # Iterator used to change player after every 3rd iteration
    loopIter = 0

    # Position of the player character on the welcome screen
    playerX = int(SCREENWIDTH * 0.2)
    playerY = int((SCREENHEIGHT - IMAGES['player'][0].get_height())/2)

    # Position of the welcome message on the welcome screen
    welcomeX = int((SCREENWIDTH - IMAGES['welcome'].get_width())/2)
    welcomeY = int(SCREENHEIGHT * 0.2)

    # Setting the width of base to zero
    baseX = 0

    # The amount by which the base shift to either right or the left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # Value and direction for simple harmonic motion performed by the player character on the welcome screen
    playerShmValues = {'val': 0, 'dir': 1}

    # While loop to determine the on-screen output after first action is taken
    while True:
        for event in pygame.event.get():

        # Exiting the game if the player pressed the escape button
            if  event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Making the first jump and starting the game if the player presses space or up button
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return {
                    'playerY': playerY + playerShmValues['val'],
                    'baseX' : baseX,
                    'playerIndexGenerator' : playerIndexGenerator,
                }

        # Switching player charecter after every three times
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGenerator)
        loopIter = (loopIter + 1) % 30

        # Adjusting the base positioning on the screen
        baseX = -((-baseX + 4) % baseShift)

        # Assigning shm value to the player character
        playerShm(playerShmValues)

        # Drawing sprites with image source and coordinates
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex], (playerX, playerY + playerShmValues['val']))
        SCREEN.blit(IMAGES['message'], (messageX, messageY))
        SCREEN.blit(IMAGES['base'], (baseX, BASEY))

        # Updating the display using pygame library
        pygame.display.update()

        # Setting the frames per second for the display
        FPSCLOCK.tick(FPS)



#Sunny
def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGenerator = movementInfo['playerIndexGenerator']
    playerX, playerY = int(SCREENWIDTH * 0.2), movementInfo['playerY']

    baseX = movementInfo['baseX']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 400, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 400 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 400, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 400 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY    =  -7   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  5   # max vel along Y, max descend speed
    playerMinVelY =  -15   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerRot     =  360   # player's rotation
    playerVelRot  =   10   # angular speed
    playerRotThr  =  15   # rotation threshold
    playerFlapAcc =  -7   # players speed on flapping
    playerFlapped = False # True when player flaps


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()

        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()

        # check for crash here
        crashTest = checkCrash({'x': playerX, 'y': playerY, 'index': playerIndex},
                               upperPipes, lowerPipes)
        if crashTest[0]:
            return {
                'y': playerY,
                'groundCrash': crashTest[1],
                'baseX': baseX,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        # check for score
        playerMidPos = playerX + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS['point'].play()

        # playerIndex baseX change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGenerator)
        loopIter = (loopIter + 1) % 30
        baseX = -((-baseX + 100) % baseShift)

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playerY += min(playerVelY, BASEY - playerY - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (baseX, BASEY))
        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerX, playerY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

#Rushi
def showGameOverScreen(crashInfo):
    """displays game over screen if the player crashes with any pipes or the base"""

    #assign the final score after the player crashes
    score = crashInfo['score']

    # position of the player character on the screen after the crash
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']

    #height, velocity, acceleration of the player character
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2

    #player chracter's rotation and rotational velocity after the crash
    playerRot = crashInfo['playerRot']
    playerVelRot = 7

    #position of the base after the crash
    basex = crashInfo['basex']

    #assigning values to the pipes after the crash
    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    # While loop to determine the on-screen output after the crash
    while True:
        for event in pygame.event.get():

        # Exiting the game if the player pressed the escape button
            if  event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # returning to the beginning of the gameif the player presses space or up button
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprite for background
        SCREEN.blit(IMAGES['background'], (0,0))

        #drawing sprites for upper and lower pipes
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        #drawing sprite for the base and showing the score
        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        #rotating the player character image after the crash and blitting it to the screen
        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))

        #drwaing sprite for the game over message
        SCREEN.blit(IMAGES['gameover'], (50, 180))

        #setting the frames per second for the display
        FPSCLOCK.tick(FPS)

        #updating the display using pygame library
        pygame.display.update()




#Kizar
def showScore(score):
    scoreDigi = []
    numWidth = 0

    for x in list(str(score)):

        scoreDigi.append(int(x))

    for digit in scoreDigi:
        numWidth += IMAGES['numbers'][digit].get_width()

        scoreDigi.append(int(x))

    for digit in scoreDigi:
        numWidth += IMAGES['numbers'][digit].get_width()


    offSetX = (SCREENWIDTH - numWidth) /  2

    for digit in scoreDigi:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        offSetX += IMAGES['numbers'][digit].get_width()

#Sunny
def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 9:
        playerShm['dir'] *= -2

    if playerShm['dir'] == 2:
         playerShm['val'] += 2
    else:
        playerShm['val'] -= 2
#Rushi
def getRandomPipe():
    """this function returns a randomly generated pipe"""

    # generating the random y gap between the pipes
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    #returning the new coordinates for randomly generated upper and lower pipes
    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # for the upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # for the lower pipe
    ]


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

import random
import pygame, sys
from pygame.locals import *
import time
from datetime import timedelta

gamemap = []
logicmap = []

# bomb image
bombImg = pygame.image.load('bomb.png')
bombImg = pygame.transform.scale(bombImg, (25, 25))

# Pygame is able to load images onto Surface objects from PNG, JPG, GIF, and BMP image files.
numbersImg = pygame.image.load('numbers_1_8.png')
# scale image
numbersImg = pygame.transform.scale(numbersImg, (100, 50))

# uncovered cell image
uncoveredImg = pygame.image.load('uncovered.png')
uncoveredImg = pygame.transform.scale(uncoveredImg, (25, 25))

#empty  cell image
emptyImg = pygame.image.load('empty.png')
emptyImg = pygame.transform.scale(emptyImg, (25, 25))

# uncovered cell image
flagImg = pygame.image.load('flag.png')
flagImg = pygame.transform.scale(flagImg, (25, 25))

bombsRevealed = 0

starttime = 0
currenttime = 0

#button

numberSurfaces = []

for y in range(0,2):
    for x in range(0,4):
        number = pygame.Surface((25.0, 25.0))
        numberSurfaces.append(number)
        numberSurfaces[-1].blit(numbersImg, (0, 0), (x * float(25.0), y * float(25.0), 25.0, 25.0))

print("numbers = {0}".format(numberSurfaces))
clickCounter = 0
shortneighbors = 0
def InitializeMap(remainingCells, remainingbombs):
    for y in range(16):

        maprow = []
        gamemaprow= []
        for x in range(16):

            gamemaprow.append(uncoveredImg)
            randNumber = random.randint(1, remainingCells)
            if randNumber <= remainingbombs:
                maprow.append('bomb')
                remainingbombs -= 1
            else:
                maprow.append('uncovered')
            remainingCells -= 1

        logicmap.append(maprow)
        gamemap.append(gamemaprow)

    print("INITIALIZED!")

def GetNeighborCells(y,x):
    neighbors = []

    global shortneighbors

    #print("{0},{1}".format(y,x))
    for _y in range(y-1,y+2):
        for _x in range(x-1,x+2):
            add = True
            if _y == y and _x == x:
                add = False
            if _y < 0 or _y > 15:
                add = False
            if _x < 0 or _x > 15:
                add = False

            if add:
                neighbors.append((_y,_x))
    return neighbors

def HasAdjacentBombs(y,x):
    neighbors = GetNeighborCells(y,x)

    adjacentBombs = 0

    for neighbor in neighbors:
        #if logicmap[neighbor[0]][neighbor[1]] != 'empty' and logicmap[neighbor[0]][neighbor[1]] != 'uncovered':

        if logicmap[neighbor[0]][neighbor[1]] == 'bomb':
            print("bomb coords = {0},{1}".format(neighbor[0],neighbor[1]))
            adjacentBombs += 1

    if adjacentBombs > 0:
        #print("current coords: {0},{1} has {2} neighbors!".format(y,x,len(neighbors)))
        return True, adjacentBombs

    return False, 0

def UnCoverCell(y, x):

    global clickCounter
    clickCounter += 1
    #print("clickcounter = {0}" .format(clickCounter))

    if logicmap[y][x] == 'empty':
        return

    result = HasAdjacentBombs(y, x)
    logicmap[y][x] = 'empty'
    if result[0] == False or clickCounter == 1:

        if clickCounter == 1:
            print("adjacent bombs(exp 0): {0}, clickCounter: {1}".format(result[1], clickCounter))
        gamemap[y][x] = emptyImg
        if result[1] == 1:
            gamemap[y][x] = numberSurfaces[0]
        elif result[1] == 2:
            gamemap[y][x] = numberSurfaces[1]
        elif result[1] == 3:
            gamemap[y][x] = numberSurfaces[2]
        elif result[1] == 4:
            gamemap[y][x] = numberSurfaces[3]
        elif result[1] == 5:
            gamemap[y][x] = numberSurfaces[4]
        elif result[1] == 6:
            gamemap[y][x] = numberSurfaces[5]
        elif result[1] == 7:
            gamemap[y][x] = numberSurfaces[6]
        elif result[1] == 8:
            gamemap[y][x] = numberSurfaces[7]

        for neighbor in GetNeighborCells(y, x):
            if logicmap[neighbor[0]][neighbor[1]] != 'bomb' and logicmap[neighbor[0]][neighbor[1]] != 'empty':
                UnCoverCell(neighbor[0], neighbor[1])

    else:
        if result[1] == 1:
            gamemap[y][x] = numberSurfaces[0]
        elif result[1] == 2:
            gamemap[y][x] = numberSurfaces[1]
        elif result[1] == 3:
            gamemap[y][x] = numberSurfaces[2]
        elif result[1] == 4:
            gamemap[y][x] = numberSurfaces[3]
        elif result[1] == 5:
            gamemap[y][x] = numberSurfaces[4]
        elif result[1] == 6:
            gamemap[y][x] = numberSurfaces[5]
        elif result[1] == 7:
            gamemap[y][x] = numberSurfaces[6]
        else:
            gamemap[y][x] = numberSurfaces[7]

def buttonify(Picture, coords, surface):
    image = pygame.image.load(Picture)
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    return (image,imagerect)


def RepositionBomb(y, x):

    logicmap[y][x] = "uncovered"

    while True:
        randX = random.randint(0, 15)
        randY = random.randint(0, 15)

        if logicmap[randY][randX] != "bomb":
            logicmap[randY][randX] = "bomb"
            #gamemap[randY][randX] = bombImg
            break

pygame.init()

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 450), 0, 32)
pygame.display.set_caption('MineSweeper')

WHITE = (255, 255, 255)

mapInitialized = False

bombcount = 30
remainingbombs = bombcount
remainingCells = 16*16
remainingCellsStart = remainingCells

fontObj = pygame.font.Font('freesansbold.ttf',32)

while True:  # the main game loop
    DISPLAYSURF.fill(WHITE)

    # Blitting is drawing the contents of one Surface onto another. It is done with the blit() Surface object method.
    # surf.blit( my_image, (A, B), (C, D, E, F) )
    # (a,b) = distance from top left corner
    # (c,d) = cropped part of image from tl corner
    # (e,f) = image size
    #DISPLAYSURF.blit(numbersImg, (0,0), (0,0,25,25))
    #DISPLAYSURF.blit(numbersImg, (25,0), (25, 0, 25, 25))
    #DISPLAYSURF.blit(numbers[1], (1* 25.0, y * 25.0), (0.0, 0.0, 25.0, 25.0))

    #Initialize game map

    if not mapInitialized:
        mapInitialized = True
        InitializeMap(remainingCells,remainingbombs)

    #Display game map
    for y in range(16):
        for x in range(16):
            DISPLAYSURF.blit(gamemap[y][x], (x * 25.0, y * 25.0))

    #Display flag img in lower left corner
    DISPLAYSURF.blit(flagImg, (14, 410))

    #Update and render game timer
    currentTime = int(time.time())

    if clickCounter > 0 :
        elapsedTime = currentTime - starttime
    else:
        starttime = currentTime

    hours, rem = divmod(currentTime- starttime, 3600)
    minutes, seconds = divmod(rem, 60)

    textSurfaceObj = fontObj.render(str(minutes) + ":" + str(seconds), True, (0, 255, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (350, 425)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    #render bombs revealed
    textSurfaceObj = fontObj.render(str(bombsRevealed) + "/" + str(bombcount), True, (0, 255, 0))
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (75, 425)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    #Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:

            x, y = event.pos
            xIndex = int(x / 25)
            yIndex = int(y / 25)

            if event.button == 1:
                if logicmap[yIndex][xIndex] != 'bomb':
                    UnCoverCell(yIndex,xIndex)

                #if logicmap[yIndex][xIndex] == 'bomb':
                elif clickCounter == 0:
                    print("First click on bomb!")
                    RepositionBomb(yIndex, xIndex)
                    UnCoverCell(yIndex, xIndex)
                else:
                    gamemap[yIndex][xIndex] = bombImg

            elif event.button == 3:
                if gamemap[yIndex][xIndex] == uncoveredImg:
                    gamemap[yIndex][xIndex] = flagImg

                    if logicmap[yIndex][xIndex] == 'bomb':
                        bombsRevealed+=1

                elif gamemap[yIndex][xIndex] == flagImg:
                    gamemap[yIndex][xIndex] = uncoveredImg
                    if logicmap[yIndex][xIndex] == 'bomb':
                        bombsRevealed-=1


    pygame.display.update()
    fpsClock.tick(FPS)

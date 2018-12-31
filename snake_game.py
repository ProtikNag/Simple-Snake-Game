import pygame, sys, random, time
from pygame.locals import *

WINDOWHEIGHT =  600
WINDOWWIDTH  = 1000
FPS          =   10
CELLHEIGHT   =   20
CELLWIDTH    =   20
CELLNUMBER_X = int(WINDOWWIDTH / CELLWIDTH)
CELLNUMBER_Y = int(WINDOWHEIGHT / CELLHEIGHT)

assert WINDOWWIDTH % CELLWIDTH == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLHEIGHT == 0, "Window height must be a multiple of cell size."

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKGREEN = (  0, 255,   0)
GREEN     = (  0, 155,   0)
GRAY      = (128, 128, 128)
BLUE      = (  0,   0, 255)
YELLOW    = (253, 210,  37)
CYAN      = (  4, 222, 178)
TEAL      = (  0, 128, 128)
FIREBRICK = ( 178, 34,  34)
SILVER    = (192, 192, 192)
DARKGRAY  = ( 30,  30,  30)
SEAGREEN  = ( 32, 178,  70)
BGCOLOR   = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


hurdle =     ({'x': 5,    'y': 5}, {'x':16,    'y': 5}, {'x':34,    'y': 5},
              {'x': 5,    'y': 6}, {'x':16,    'y':24}, {'x':34,    'y':24},
              {'x': 5,    'y':23}, {'x':16,    'y': 6}, {'x':42,    'y': 5},
              {'x': 5,    'y':24}, {'x':16,    'y':23}, {'x':42,    'y':24},
              {'x': 6,    'y': 5}, {'x':33,    'y': 5}, {'x':43,    'y': 5},
              {'x': 6,    'y':24}, {'x':33,    'y': 6}, {'x':43,    'y': 6},
              {'x':15,    'y': 5}, {'x':33,    'y':23}, {'x':43,    'y':23},
              {'x':15,    'y':24}, {'x':33,    'y':24}, {'x':43,    'y':24},
              {'x':10,    'y':14}, {'x':38,    'y':14}, {'x':11,    'y':14},
              {'x':10,    'y':15}, {'x':38,    'y':15}, {'x':39,    'y':14},
              {'x':11,    'y':15}, {'x':39,    'y':15})

visited = [[False for y in range(30)] for y in range(50)]



def main():

    #create the highscore.txt file
    try:
        file = open("highscore.txt", 'r')
    except IOError:
        file = open("highscore.txt", 'w')
    file.close()

    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake Mania')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    makeVisited()
    startPage()

    while True:

        score = runGame()
        gameOverPage(score)

        

def runGame():

    startx = 25
    starty = 15

    startingDirections = (UP,DOWN,LEFT,RIGHT)

    index = random.randint(0,3)
    direction = startingDirections[index]

    wormCoordinates = getCoordinates(direction,startx,starty)

    food = getRandomLocation()
    color = RED

    scoreCounter = 0

    while True:

        inc = 0

        for event in pygame.event.get():
    
            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif event.key == K_ESCAPE:
                    terminate()

            inc += 1

            if inc > 0:
                break
        
        if gameOver(wormCoordinates) == True or hurdleCollision(wormCoordinates) == True:
            soundObj = pygame.mixer.Sound('gameOver.wav')
            soundObj.play()
            time.sleep(1)
            soundObj.stop()
            compareScore(scoreCounter)
            pygame.time.wait(1000)
            return scoreCounter

        #  Check if snake has eaten food

        if wormCoordinates[0]['x'] == food['x'] and wormCoordinates[0]['y'] == food['y']:

            soundObj = pygame.mixer.Sound('beep.wav')
            soundObj.play()
            
            food = getRandomLocation()

            if color == RED:
                scoreCounter += 2
            elif color == BLUE:
                scoreCounter += 5
            elif color == YELLOW:
                scoreCounter += 7

            foodColor = (YELLOW,RED,BLUE)

            index = random.randint(0,2)
            color = foodColor[index]
            
        else:   
            del wormCoordinates[-1]


        wormCoordinates = moveWorm(wormCoordinates,direction)
        

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawFood(food,color)
        drawScore(scoreCounter)
        drawWorm(wormCoordinates,direction)
        drawHurdles()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def makeVisited():

    for row in range(50):
        for col in range(30):
            has = False
            for hard in hurdle:
                if hard['x'] == row and hard['y'] == col:
                    has = True
                    break
            if has == True:
                visited[row][col] = True
            else :
                visited[row][col] = False
            


def drawHurdles():

    for hard in hurdle:

        x = hard['x'] * CELLWIDTH
        y = hard['y'] * CELLHEIGHT

        hardRect = pygame.Rect(x,y,CELLHEIGHT,CELLWIDTH)
        pygame.draw.rect(DISPLAYSURF,SILVER,hardRect)



def hurdleCollision(wormCoordinates):

    xx = wormCoordinates[0]['x']
    yy = wormCoordinates[0]['y']

    if visited[xx][yy] == True:
        return True

    return False


def drawFood(food,color):
    
    x = food['x'] * CELLWIDTH
    y = food['y'] * CELLHEIGHT

    foodRect = pygame.Rect(x,y,CELLHEIGHT,CELLWIDTH)
    pygame.draw.rect(DISPLAYSURF,color,foodRect)



def drawScore(score):

    scoreSurf = BASICFONT.render('Score: %s' % (score), True, YELLOW)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-120,10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)



def moveWorm(wormCoordinates,direction):

    if direction == LEFT:
        newHead = {'x': wormCoordinates[0]['x']-1,  'y': wormCoordinates[0]['y']}
    elif direction == RIGHT:
        newHead = {'x': wormCoordinates[0]['x']+1,  'y': wormCoordinates[0]['y']}
    elif direction == UP:
        newHead = {'x': wormCoordinates[0]['x'],    'y': wormCoordinates[0]['y']-1}
    elif direction == DOWN:
        newHead = {'x': wormCoordinates[0]['x'],    'y': wormCoordinates[0]['y']+1} 


    wormCoordinates.insert(0,newHead)

    return wormCoordinates


    
def gameOver(wormCoordinates):

    if wormCoordinates[0]['x'] == -1 or wormCoordinates[0]['x'] == CELLNUMBER_X:
        return True
    elif wormCoordinates[0]['y'] == -1 or wormCoordinates[0]['y'] == CELLNUMBER_Y:
        return True
    else:
        for cords in wormCoordinates[1:]:
            if cords['x'] == wormCoordinates[0]['x'] and cords['y'] == wormCoordinates[0]['y']:
                return True

    return False
  


def drawWorm(wormCoordinates,direction):

    count = 0

    for coord in wormCoordinates:
        x = coord['x'] * CELLHEIGHT
        y = coord['y'] * CELLWIDTH

        wormSegmentRect = pygame.Rect(x,y,CELLHEIGHT,CELLWIDTH)
        pygame.draw.rect(DISPLAYSURF,GREEN,wormSegmentRect)

        wormInnerSegmentRect = pygame.Rect(x+4,y+4,CELLHEIGHT-8,CELLWIDTH-8)
        pygame.draw.rect(DISPLAYSURF,DARKGREEN,wormInnerSegmentRect)

        if count == 0:
            if direction == LEFT:
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+5),int(y+5)), 4, 0)
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+5),int(y+15)), 4, 0)
            elif direction == RIGHT:
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+15),int(y+5)), 4, 0)
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+15),int(y+15)), 4, 0)
            elif direction == UP:
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+5),int(y+5)), 4, 0)
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+15),int(y+5)), 4, 0)
            elif direction == DOWN:
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+5),int(y+15)), 4, 0)
                wormEyesCircle = pygame.draw.circle(DISPLAYSURF, RED, (int(x+15),int(y+15)), 4, 0)

            
        count += 1



def drawGrid():

    for x in range(0, WINDOWWIDTH, CELLWIDTH):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0), (x,WINDOWWIDTH))
    for y in range(0, WINDOWHEIGHT, CELLHEIGHT):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH,y))



def getRandomLocation():

    while True:
        
        x_pos = random.randint(0,CELLNUMBER_X - 1)
        y_pos = random.randint(0,CELLNUMBER_Y - 1)

        if visited[x_pos][y_pos] == False:
            return {'x': x_pos,   'y':y_pos}



def terminate():

    pygame.quit()
    sys.exit()



def getCoordinates(direction,startx,starty):

    if direction == UP:
        retCoordinates = [{'x': startx,     'y': starty},
                          {'x': startx,     'y': starty+1},
                          {'x': startx,     'y': starty+2}]
    elif direction == DOWN:
        retCoordinates = [{'x': startx,     'y': starty},
                          {'x': startx,     'y': starty-1},
                          {'x': startx,     'y': starty-2}]
    elif direction == LEFT:
        retCoordinates = [{'x': startx,     'y': starty},
                          {'x': startx+1,   'y': starty},
                          {'x': startx+2,   'y': starty}]
    elif direction == RIGHT:
        retCoordinates = [{'x': startx,     'y': starty},
                          {'x': startx-1,   'y': starty},
                          {'x': startx-2,   'y': starty}]
        
        

    return retCoordinates



def startPage():

    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake', True, RED)
    titleSurf2 = titleFont.render('Mania', True, CYAN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        highScoreButton = button(BLUE,140,WINDOWHEIGHT-35,100,25,'High Scores')
        highScoreButton.draw(DISPLAYSURF,15,RED)

        creditsButton = button(CYAN,20,WINDOWHEIGHT-35,100,25,'Credits')
        creditsButton.draw(DISPLAYSURF,15,BLUE)

        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if highScoreButton.isOver(pos):
                    soundObj = pygame.mixer.Sound('button.wav')
                    soundObj.play()
                    highScorePage(0)
                    
                elif creditsButton.isOver(pos):
                    soundObj = pygame.mixer.Sound('button.wav')
                    soundObj.play()
                    creditsPage()
                    
            elif event.type == pygame.MOUSEMOTION:
                if highScoreButton.isOver(pos):
                    highScoreButton.color = FIREBRICK
                    highScoreButton.draw(DISPLAYSURF,15,WHITE)
                else:
                    highScoreButton.color = BLUE
                    highScoreButton.draw(DISPLAYSURF,15,RED)
                if creditsButton.isOver(pos):
                    creditsButton.color = YELLOW
                    creditsButton.draw(DISPLAYSURF,15,CYAN)
                else:
                    creditsButton.color = CYAN
                    creditsButton.draw(DISPLAYSURF,15,BLUE)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

            

def gameOverPage(score):

    DISPLAYSURF.fill(BGCOLOR)

    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    scoreFont = pygame.font.Font('freesansbold.ttf', 50)
    luckFont = pygame.font.Font('freesansbold.ttf', 40)

    gameOverSurf = gameOverFont.render('Game Over',True,WHITE)
    scoreSurf = scoreFont.render('Score: %s' % (score),True,YELLOW)
    luckSurf = luckFont.render('Better Luck Next Time',True,CYAN)
    
    gameOverRect  = gameOverSurf.get_rect()
    scoreRect = scoreSurf.get_rect()
    luckRect  = luckSurf.get_rect()

    gameOverRect.midtop  = (500,10)
    scoreRect.midtop     = (500,150)
    luckRect.midtop      = (500,300)

    DISPLAYSURF.blit(gameOverSurf, gameOverRect)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    DISPLAYSURF.blit(luckSurf, luckRect)

    highScoreButton = button(BLUE,370,400,250,100,'High Scores')
    highScoreButton.draw(DISPLAYSURF,35,RED)

    creditsButton = button(CYAN,20,WINDOWHEIGHT-35,100,25,'Credits')
    creditsButton.draw(DISPLAYSURF,15,BLUE)

    drawPressKeyMsg()

    pygame.display.update()
    pygame.time.wait(500)

    while True:

        pygame.display.update()
        
        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()
            
            if event.type == QUIT:
                terminate()
                
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    return
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if highScoreButton.isOver(pos):
                    soundObj = pygame.mixer.Sound('button.wav')
                    soundObj.play()
                    highScorePage(score)
                    return
                elif creditsButton.isOver(pos):
                    soundObj = pygame.mixer.Sound('button.wav')
                    soundObj.play()
                    creditsPage()
                    return 
                    
            elif event.type == pygame.MOUSEMOTION:
                if highScoreButton.isOver(pos):
                    highScoreButton.color = FIREBRICK
                    highScoreButton.draw(DISPLAYSURF,35,WHITE)
                else:
                    highScoreButton.color = BLUE
                    highScoreButton.draw(DISPLAYSURF,35,RED)
                if creditsButton.isOver(pos):
                    creditsButton.color = YELLOW
                    creditsButton.draw(DISPLAYSURF,15,CYAN)
                else:
                    creditsButton.color = CYAN
                    creditsButton.draw(DISPLAYSURF,15,BLUE)



class button():
    def __init__(self,color,x,y,width,height,text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,fontsize,outline=None):

        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.Font('freesansbold.ttf', fontsize)
            text = font.render(self.text, 1, BLACK)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False




def compareScore(score):

    highScores = [score]

    fileObj = open("highscore.txt",'r+')
    lines = fileObj.readlines()
    
    for line in lines:          
       conv_int = int(line)
       highScores.append(conv_int)

    highScores = list(set(highScores))

    highScores.sort(reverse=True)
    newHighScores = []

    count = 0
    for sc in highScores:

        newHighScores.append(sc)
        count += 1

        if count == 5:
            break

    fileObj.seek(0)
    fileObj.truncate()  # removes everything written in the file

    for sc in newHighScores:

        fileObj.write(str(sc))
        fileObj.write('\n')

    fileObj.close()


def highScorePage(score):

    DISPLAYSURF.fill(BGCOLOR)

    drawPressKeyMsg()

    highScoreFont = pygame.font.Font('freesansbold.ttf', 100)
    highScoreSurf = highScoreFont.render('High Scores',True,WHITE)
    highScoreRect  = highScoreSurf.get_rect()
    highScoreRect.midtop  = (500,10)

    DISPLAYSURF.blit(highScoreSurf,highScoreRect)

    highScores = []

    fileObj = open("highscore.txt",'r')
    lines = fileObj.readlines()
    
    for line in lines:          
       conv_int = int(line)
       if conv_int == 0:
           continue
       highScores.append(conv_int)

    count    =   1
    gap      =  70
    constant = 200

    for sc in highScores:

        scoreListFont = pygame.font.Font('freesansbold.ttf', 35)
        scoreListSurf = scoreListFont.render('%d'  %(sc),True,WHITE)
        scoreListRect = scoreListSurf.get_rect()
        scoreListRect.midtop = (500,(constant+(count-1)*gap))
        DISPLAYSURF.blit(scoreListSurf,scoreListRect)
        count += 1

    fileObj.close()

    while True:

        pygame.display.update()

        for event in pygame.event.get():

            pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    return



def creditsPage():

    DISPLAYSURF.fill(BGCOLOR)

    drawPressKeyMsg()

    creditsFont = pygame.font.Font('freesansbold.ttf', 100)
    creditsSurf = creditsFont.render('CREDITS',True,WHITE)
    creditsRect  = creditsSurf.get_rect()
    creditsRect.midtop  = (500,10)

    supervisorFont = pygame.font.Font('freesansbold.ttf', 35)
    supervisorSurf = supervisorFont.render('Supervisor',True,WHITE)
    supervisorRect  = supervisorSurf.get_rect()
    supervisorRect.midtop  = (200,150)

    sirNameFont = pygame.font.Font('freesansbold.ttf', 20)
    sirNameSurf = sirNameFont.render('Md Saiful Islam, Assistant Professor, Department of CSE, SUST',True,WHITE)
    sirNameRect  = sirNameSurf.get_rect()
    sirNameRect.midtop  = (500,250)

    developFont = pygame.font.Font('freesansbold.ttf', 35)
    developSurf = developFont.render('Developed by',True,WHITE)
    developRect  = developSurf.get_rect()
    developRect.midtop  = (220,350)

    myNameFont = pygame.font.Font('freesansbold.ttf', 20)
    myNameSurf = myNameFont.render('Protik Nag, Department of CSE, SUST',True,WHITE)
    myNameRect  = myNameSurf.get_rect()
    myNameRect.midtop  = (360,450)

    DISPLAYSURF.blit(creditsSurf,creditsRect)
    DISPLAYSURF.blit(supervisorSurf,supervisorRect)
    DISPLAYSURF.blit(sirNameSurf,sirNameRect)
    DISPLAYSURF.blit(developSurf,developRect)
    DISPLAYSURF.blit(myNameSurf,myNameRect)

    while True:

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == QUIT:
                terminate()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    return



def drawPressKeyMsg():

    pressKeySurf = BASICFONT.render('Press Spacebar to Play',True,GRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH-250,WINDOWHEIGHT-30)
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)


if __name__ == '__main__':
    main()
    
    

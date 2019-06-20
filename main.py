from snake import Snake,playersHandler
from config import config
from orb import orbFactory,updateAndDisplayOrbs
import pygame as pg
from menu import Button

tickNumber=0
gameLength=config.gameLength
frameRate=config.frameRate
screenSize=config.screenSize
orbFactory.initalizePools()
gameDisplay = pg.display.set_mode((config.screenSize[0], config.screenSize[1]))
pg.init()
pg.display.set_caption("")

def getControls():
    keys=pg.key.get_pressed()
    return((keys[pg.K_w],keys[pg.K_a],keys[pg.K_s],keys[pg.K_d],keys[pg.K_UP],keys[pg.K_LEFT],keys[pg.K_DOWN],keys[pg.K_RIGHT]))
#snake inputs are as follows
#playerNumber,startingSpeed,turningRadius,startingLength,segmentLength,dashDistance
def gameLoop(p1,p2,clock,tickNumber):
    while not (p1.dead or p2.dead or config.quit):
        #print(clock)
        tickNumber+=1
        keys=getControls()
        playersHandler(p1,p2,keys,gameDisplay,tickNumber)
        updateAndDisplayOrbs(orbFactory,(p1,p2),gameDisplay,tickNumber)
        if tickNumber%gameLength==0:
            p1.dead=True
            p2.dead=True

        if tickNumber%config.orbFactoryCallPeriod==0:
            print("orbFactory called")
            orbFactory.spawnHandler(tickNumber,(p1,p2))


        clock.tick_busy_loop(frameRate)
        pg.display.update()
        #if not p1.lastTickDashed-tickNumber==0:
        #    pg.Surface.fill(gameDisplay,(0,0,0))

        #this improves visual effect of dashing by not filling the screen for the tick of a dash
        if not (p1.lastTickDashed-tickNumber==0 or p2.lastTickDashed-tickNumber==0):
            pg.Surface.fill(gameDisplay,(0,0,0))

        if p1.dead:
            print("player 1 died")

        if p2.dead:
            print("player 2 died")

def startGame(clock,p1,p2):
    gameLoop(p1,p2,clock,tickNumber)

    orbFactory.resetPools()

def startScreen(clock):
    
    startButton=Button((screenSize[0]/2,screenSize[1]/2),250,250,[],(255,255,255),False)

    p1=Snake(1,3,100,5,20,100)
    p1.createSnake()

    p2=Snake(2,3,100,5,20,100)
    p2.createSnake()

    while not (startButton.wasPressed or config.quit):
        for event in pg.event.get():
            # checks if player has quit
            if event.type == pg.QUIT:
                config.quit=True
        pg.Surface.fill(gameDisplay,(0,0,0))
        playersHandler(p1,p2,(0,1,0,0,0,1,0,0),gameDisplay,0)


        clock.tick_busy_loop(frameRate)
        
        mousePos=pg.mouse.get_pos()
        mousePressed=pg.mouse.get_pressed()
        mouseIsOnButton=startButton.displayAndGetClicked(mousePos,mousePressed,gameDisplay)
        if mouseIsOnButton:
            p1.color=(255,0,0)
            p2.color=(255,0,0)
        else:
            p1.color=(255,255,255)
            p2.color=(255,255,255)
        pg.display.update()
    
    p1.color=(255,0,0)
    p2.color=(255,0,0)
    p1.changeTurningRadius(config.turningRadius)
    p2.changeTurningRadius(config.turningRadius)
    return(p1,p2)

def main():
    while not config.quit:
        clock = pg.time.Clock()
        p1,p2=startScreen(clock)
        startGame(clock,p1,p2)

main()
pg.quit()
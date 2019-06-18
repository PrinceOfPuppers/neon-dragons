import pygame as pg
from math import sin,cos,pi
import numpy as np
from config import config
import orb as rb


pg.init()
pg.display.set_caption("Snake 360")
clock = pg.time.Clock()
screenSize=config.screenSize
frameRate=config.frameRate
tickNumber=0
gameDisplay = pg.display.set_mode((screenSize[0], screenSize[1]))
gameOver=False
gameLength=config.gameLength




def doLineSegmentsIntersect(line1Point1,line1Point2,line2Point1,line2Point2):
    vec1x=line1Point2[0]-line1Point1[0]
    vec1y=line1Point2[1]-line1Point1[1]

    vec2x=line2Point2[0]-line2Point1[0]
    vec2y=line2Point2[1]-line2Point1[1]

    M=np.array([[vec1x,-vec2x],[vec1y,-vec2y]])
    if np.linalg.det(M)==0:
        return(False)
    b=np.array([line2Point1[0]-line1Point1[0],line2Point1[1]-line1Point1[1]])

    scalingFactors=np.linalg.solve(M,b)
    
    if (0<=scalingFactors[0] and scalingFactors[0]<=1) and (0<=scalingFactors[1] and scalingFactors[1]<=1):
        return(True)
    return(False)

def didEatOtherSnake(snake1,snake2):

    snake1Index2=snake1.headIndexInPosistionList
    snake1Index1=(snake1.headIndexInPosistionList-snake1.segmentLength)%snake1.positionListLength

    snake1Point2=snake1.previousPosistions[snake1Index2]
    snake1Point1=snake1.previousPosistions[snake1Index1]
    #pg.draw.aaline(gameDisplay,(255,255,255),snake1Point1,snake1Point2)
    for i in range(0,snake2.length-1):
        
        snake2Index1=(i*snake2.segmentLength+snake2.headIndexInPosistionList+1)%snake2.positionListLength
        snake2Index2=((i+1)*snake2.segmentLength+snake2.headIndexInPosistionList)%snake2.positionListLength

        snake2Point1=snake2.previousPosistions[snake2Index1]
        snake2Point2=snake2.previousPosistions[snake2Index2]
        colorMod=i/snake2.length
        pg.draw.aaline(gameDisplay,(int(255*colorMod),int(255*colorMod),255),snake2Point1,snake2Point2)
        if doLineSegmentsIntersect(snake1Point1,snake1Point2,snake2Point1,snake2Point2):
            #mutual eat
            if i+1==snake2.length-1:
                snake1.changeSnakeSize(1)
                snake2.changeSnakeSize(1)
                return(True,True)
            
            #snake2 ate snake 1
            else:
                snake2.changeSnakeSize(snake2.length-i-1)
                return(True,False)
    return(False,False)

def getAndApplyControls(p1,p2,tickNumber,gameOver):
    for event in pg.event.get():
        # checks if player has quit
        if event.type == pg.QUIT:
            return(True)
    
    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()


    #p1 controls
    if keys[pg.K_a]:
        p1.rot+=p1.rotVel
    if keys[pg.K_d]:
        p1.rot-=p1.rotVel
    
    #dashes the player
    if keys[pg.K_w]:
        p1.dash(p2,tickNumber)


    #p2 controls
    if keys[pg.K_LEFT]:
        p2.rot+=p2.rotVel
    if keys[pg.K_RIGHT]:
        p2.rot-=p2.rotVel

    if keys[pg.K_UP]:
        p2.dash(p1,tickNumber)
    return(gameOver)

def playersHandler(players,gameOver):
    #applys all player operations for a single tick

    p1=players[0]
    p2=players[1]
    p1.updateAndDisplay(p2,screenSize)
    p2.updateAndDisplay(p1,screenSize)
    gameOver=getAndApplyControls(p1,p2,tickNumber,gameOver)
    if p1.dead:
        print("player 1 died")
        gameOver=True
    if p2.dead:
        print("player 2 died")
        gameOver=True
    return(gameOver)

class Snake:
    #the snake consists of a number of segments who follow the previous path of the head of the snake, the segment length just determines how many ticks ago they follow
    #the position of the snake each tick are recorded each tick to a list, the length of which is dynamically increased depending on how long the snake is
    def __init__(self,playerNumber,startingSpeed,rotVel,startingLength,segmentLength,dashDistance):
        #length refers to number of segments
        self.dead=False
        self.playerNumber=playerNumber
        self.length=startingLength
        self.position=[0,0]
        self.rot=0
        self.rotVel=rotVel
        self.speed=startingSpeed
        self.segmentLength=segmentLength
        self.dashDistance=dashDistance
        self.lastTickDashed=-100
        self.dashCoolDown=100
        #these are all updated in create snake
        #the list oldest entry in the list is updated, so the poisistion of the head must be recorded and is incremeted each tick
        #this way only one element of the list must be changed each tick, a list is used becasuse we will have to increase the size
        #as parameters of the snake are changed (ie length)
        self.previousPosistions=[]
        self.positionListLength=0
        self.headIndexInPosistionList=0

    def createSnake(self,screenSize):
        #generates a list for recording the previous positions 
        self.positionListLength=(self.length-1)*self.segmentLength+1
        self.headIndexInPosistionList=self.positionListLength-1
        for i in range(0,self.positionListLength):
            #extrpolates where the head would be i ticks ago so the snake doesnt start bunched up
            if self.playerNumber==1:
                self.position=[screenSize[0]/3,screenSize[1]/2]
                positionOfHeadPreviously=[self.position[0],self.position[1]-(self.positionListLength-i)*self.speed]
                self.previousPosistions.append(positionOfHeadPreviously)
            
            if self.playerNumber==2:
                self.rot=pi
                self.position=[2*screenSize[0]/3,screenSize[1]/2]
                positionOfHeadPreviously=[self.position[0],self.position[1]+(self.positionListLength-i)*self.speed]
                self.previousPosistions.append(positionOfHeadPreviously)

    def changeSnakeSize(self,newSize):
        sizeDifference=newSize-self.length
        self.length=newSize
        #removes entries from position list and updates the index of the head in the list
        if sizeDifference<=0:
            previousPosistionListLen=self.positionListLength
            numberOfEntriesToRemove=(-1*self.segmentLength*sizeDifference)

            if numberOfEntriesToRemove+self.headIndexInPosistionList<previousPosistionListLen:

                upperIndexToDelete=self.headIndexInPosistionList+numberOfEntriesToRemove
                deleteTotal=abs(self.headIndexInPosistionList+1 -1*(upperIndexToDelete+1))
                del self.previousPosistions[self.headIndexInPosistionList+1 : upperIndexToDelete+1]


            else:

                del self.previousPosistions[self.headIndexInPosistionList+1:previousPosistionListLen]

                upperIndexToDelete=(self.headIndexInPosistionList+numberOfEntriesToRemove)%previousPosistionListLen
                deleteTotal=abs(self.headIndexInPosistionList+1-previousPosistionListLen)+abs(upperIndexToDelete+1)
                del self.previousPosistions[0:upperIndexToDelete+1]

                self.headIndexInPosistionList-=(self.headIndexInPosistionList+numberOfEntriesToRemove+1)%previousPosistionListLen
            
            self.positionListLength=len(self.previousPosistions)
            
            if not self.positionListLength==self.segmentLength*(self.length-1)+1:
                print("decreaseLength error")
        
        else:
            print(self.positionListLength)
            previousPosistionListLen=self.positionListLength
            numberOfEntriesToAdd=(self.segmentLength*sizeDifference)
            headIndex=self.headIndexInPosistionList
            
            tailIndex=(headIndex+1)%previousPosistionListLen
            tailPosition=self.previousPosistions[tailIndex]
            if tailIndex==0:
                self.headIndexInPosistionList+=numberOfEntriesToAdd

            for i in range(0,numberOfEntriesToAdd):
                point=[tailPosition[0],tailPosition[1]]
                self.previousPosistions.insert(tailIndex,point)
            
            self.positionListLength=len(self.previousPosistions)
            if not self.positionListLength==self.segmentLength*(self.length-1)+1:
                print("increaseLength error!")
        
        if self.length<=2:
            self.dead=True


        
        
    def _applyAndRecordTickMotion(self):
        self.position[0] += self.speed*sin(self.rot)
        self.position[1] += self.speed*cos(self.rot)

        self.headIndexInPosistionList+=1
        self.headIndexInPosistionList=self.headIndexInPosistionList%self.positionListLength

        self.previousPosistions[self.headIndexInPosistionList][0]=self.position[0]
        self.previousPosistions[self.headIndexInPosistionList][1]=self.position[1]

    def dash(self,other,tickNumber):
        if tickNumber-self.lastTickDashed>=self.dashCoolDown:
            for i in range(0,self.dashDistance):
                self.updateAndDisplay(other,screenSize)
                rb.updateAndDisplayOrbs(orbFactory,players,gameDisplay,tickNumber)
            
            self.lastTickDashed=tickNumber


    def updateAndDisplay(self,other,screenSize):
        self._applyAndRecordTickMotion()
        didEatOtherSnake(self,other)

        for i in range(0,self.length):
            segmentPosistionIndex=(self.headIndexInPosistionList-i*self.segmentLength)%self.positionListLength
            segmentPosistion=self.previousPosistions[segmentPosistionIndex]
            x=int(segmentPosistion[0])
            y=int(segmentPosistion[1])
            colorMod=i/self.length
            if self.playerNumber==1:
                pg.draw.circle(gameDisplay,(255,255,int(colorMod*255)),(x,y),3,1)
                
            if self.playerNumber==2:
                pg.draw.circle(gameDisplay,(255,int(colorMod*255),255),(x,y),3,1)


orbFactory=rb.OrbFactory()
orbFactory.initalizePools()

p1=Snake(1,3,0.05,5,20,100)
p1.createSnake(screenSize)

p2=Snake(2,3,0.05,5,20,100)
p2.createSnake(screenSize)

players=[p1,p2]
numberOfPlayers=len(players)
    
while not gameOver:
    #print(clock)
    tickNumber+=1
    gameOver=playersHandler(players,gameOver)
    rb.updateAndDisplayOrbs(orbFactory,players,gameDisplay,tickNumber)
    if tickNumber%gameLength==0:
        gameOver=True
    
    if tickNumber%config.orbFactoryCallPeriod==0:
        print("orbFactory called")
        orbFactory.spawnHandler(tickNumber,players)


    clock.tick_busy_loop(frameRate)
    pg.display.update()
    #if not p1.lastTickDashed-tickNumber==0:
    #    pg.Surface.fill(gameDisplay,(0,0,0))
    
    #this improves visual effect of dashing by not filling the screen for the tick of a dash
    if not (p1.lastTickDashed-tickNumber==0 or p2.lastTickDashed-tickNumber==0):
        pg.Surface.fill(gameDisplay,(0,0,0))
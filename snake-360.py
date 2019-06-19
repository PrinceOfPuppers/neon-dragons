import pygame as pg
from math import sin,cos,pi,sqrt,acos
import numpy as np
from config import config
import orb as rb
from assets import StalkerAssets


pg.init()
pg.display.set_caption("Snake 360")
clock = pg.time.Clock()
screenSize=config.screenSize
frameRate=config.frameRate
tickNumber=0
gameDisplay = pg.display.set_mode((screenSize[0], screenSize[1]))
gameLength=config.gameLength
stalkerAssets=StalkerAssets()

def rotateVector(vector,angle):
    lengthSquared=vector[0]**2+vector[1]**2
    if vector[0]!=0:
        quantity=1+(vector[1]**2)/(vector[0]**2)
        ycomp=(lengthSquared/vector[0])*(sin(angle)+(vector[1]/vector[0])*cos(angle))/quantity
        xcomp=(lengthSquared*cos(angle)-vector[1]*ycomp)/vector[0]
    elif vector[1]!=0:
        quantity=1+(vector[0]**2)/(vector[1]**2)
        xcomp=lengthSquared*((vector[0]/vector[1]*cos(angle)-sin(angle)))/(vector[1]*quantity)
        ycomp=(lengthSquared*cos(angle)-vector[0]*xcomp)/vector[1]
    else:
        return([0,0])
    return([xcomp,ycomp])

def giveAngleSigned(vec1,vec2):

    if vec1[0]==0 and vec1[1]==0:
        return(0)
    if vec2[0]==0 and vec2[1]==0:
        return(0)
    dotProd=(vec1[0]*vec2[0])+(vec1[1]*vec2[1])
    plusOrMinus1=-1
    #c determines the sign of the angle
    c=(vec1[0] * vec2[1] - vec1[1] * vec2[0]) / (sqrt((vec1[0] ** 2 + vec1[1] ** 2) * (vec2[0] ** 2 + vec2[1] ** 2)))
    if c<=0:
        plusOrMinus1=1

    #this section checks if the input for acos is within its domain (sometimes it gets rounded outside of it)
    p=dotProd/((sqrt(vec1[0]**2+vec1[1]**2))*(sqrt(vec2[0]**2+vec2[1]**2)))
    if p>1:
        p=1
    elif p<-1:
        p=-1

    theta=plusOrMinus1*acos(p)
    return(theta)

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
    
    for i in range(0,snake2.length-1):
        
        snake2Index1=(i*snake2.segmentLength+snake2.headIndexInPosistionList+1)%snake2.positionListLength
        snake2Index2=((i+1)*snake2.segmentLength+snake2.headIndexInPosistionList)%snake2.positionListLength

        snake2Point1=snake2.previousPosistions[snake2Index1]
        snake2Point2=snake2.previousPosistions[snake2Index2]
    
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

def getAndApplyControls(p1,p2,tickNumber):
    for event in pg.event.get():
        # checks if player has quit
        if event.type == pg.QUIT:
            p1.dead=True
            p2.dead=True
    
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

def playersHandler(players):
    #applys all player operations for a single tick

    p1=players[0]
    p2=players[1]
    p1.updateAndDisplay(p2,screenSize)
    p2.updateAndDisplay(p1,screenSize)
    getAndApplyControls(p1,p2,tickNumber)



class Snake:
    #the snake consists of a number of segments who follow the previous path of the head of the snake, the segment length just determines how many ticks ago they follow
    #the position of the snake each tick are recorded each tick to a list, the length of which is dynamically increased depending on how long the snake is
    def __init__(self,playerNumber,startingSpeed,turningRadius,startingLength,segmentLength,dashDistance):
        #length refers to number of segments
        self.dead=False
        self.playerNumber=playerNumber
        self.length=startingLength
        self.position=[0,0]
        self.rot=0
        self.turningRadius=turningRadius
        self.rotVel=startingSpeed/turningRadius
        self.speed=startingSpeed
        
        #segment length is the number of ticks long it is, it will change with speed
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

        #list of points currently in the snake (index zero will always be head)
        self.currentPoints=[]
        self.segmentMag=segmentLength*startingSpeed


        
        

    def grabAssets(self):
        #fits head to any segmentlength/speed combo
        self.headSkin,self.neckRadius,self.styleType,self.transformaitonLengths=stalkerAssets.scaleHead(self)
        self.headSkinMags=[]
        self.headSkinAngles=[]
        self.headSkinLen=len(self.headSkin)

        self.eye,self.iris,self.pupil=stalkerAssets.scaleEye(self)

        self.eyeMags=[]
        self.eyeAngles=[]
        self.eyeLen=len(self.eye)

        self.irisMags=[]
        self.irisAngles=[]
        self.irisLen=len(self.iris)

        self.pupilMags=[]
        self.pupilAngles=[]
        self.pupilLen=len(self.pupil)

        #prepares data regarding the head of the snake to be used by the skin rendering method
        for point in self.headSkin:
            mag=round(sqrt(point[0]**2 + point[1]**2),config.round)
            self.headSkinMags.append(mag)
            
            angle=round(giveAngleSigned(point,(0,1)),config.round)
            self.headSkinAngles.append(angle)

        #prepares data for the eye and iris
        for point in self.eye:
            mag=round(sqrt(point[0]**2 + point[1]**2),config.round)
            self.eyeMags.append(mag)
            
            angle=round(giveAngleSigned(point,(0,1)),config.round)
            self.eyeAngles.append(angle)

        for point in self.iris:
            mag=round(sqrt(point[0]**2 + point[1]**2),config.round)
            self.irisMags.append(mag)
            
            angle=round(giveAngleSigned(point,(0,1)),config.round)
            self.irisAngles.append(angle)
        
        for point in self.pupil:
            mag=round(sqrt(point[0]**2 + point[1]**2),config.round)
            self.pupilMags.append(mag)
            
            angle=round(giveAngleSigned(point,(0,1)),config.round)
            self.pupilAngles.append(angle)

        

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

        for i in range(0,self.length):
            self.currentPoints.append([0,0])
        
        self.grabAssets()


    def changeSnakeSize(self,newSize):
        sizeDifference=newSize-self.length
        self.length=newSize
        #removes entries from position list and updates the index of the head in the list
        if sizeDifference<=0:
            #removes elements from current points (points that are being displayed)
            del self.currentPoints[newSize:]

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

                for i in range(0,sizeDifference):
                    self.currentPoints.append([0,0])
                
            
            self.positionListLength=len(self.previousPosistions)
            
            if not self.positionListLength==self.segmentLength*(self.length-1)+1:
                print("decreaseLength error")
        
        else:
            #adds dummy data to current point list, they will have the correct info added in update and d
            for i in range(0,sizeDifference):
                self.currentPoints.append([0,0])
            print(self.length,len(self.currentPoints))

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

        #checks if style of snake needs to be changed
        styleType=self.styleType
        for i in range(0,len(self.transformaitonLengths)):
            transformationLength=self.transformaitonLengths[i]
            if self.length>=transformationLength:
                print("styleType increased")
                styleType+=1
                print(styleType,self.styleType)
            else:
                break
        
        if styleType!=self.styleType:
            print("grabbing assets")
            self.styleType=styleType
            self.grabAssets()

        
        
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
            self.currentPoints[i][0]=segmentPosistion[0]
            self.currentPoints[i][1]=segmentPosistion[1]
            #renders points directly from previous posisitions, rather than current point list
            if config.debug:
                x=int(segmentPosistion[0])
                y=int(segmentPosistion[1])
                colorMod=i/self.length
                if self.playerNumber==1:
                    pg.draw.circle(gameDisplay,(255,255,int(colorMod*255)),(x,y),3,1)

                if self.playerNumber==2:
                    pg.draw.circle(gameDisplay,(255,int(colorMod*255),255),(x,y),3,1)
        
        if self.length>2 and other.length>2:
            self.renderSkin(other)
        
#render eye,render stripe and render body segment are all controled by render skin
    def renderBodySegment(self,segmentNumber,previousVec,passPoints):
        bodyVec=(self.currentPoints[segmentNumber+1][0]-self.currentPoints[segmentNumber][0],self.currentPoints[segmentNumber+1][1]-self.currentPoints[segmentNumber][1])
        bodyAngle=round(giveAngleSigned(previousVec,bodyVec),config.round)
        
        
        rightBodyPoint=(-1*previousVec[1]*self.neckRadius/self.segmentMag,previousVec[0]*self.neckRadius/self.segmentMag)
        leftBodyPoint=(previousVec[1]*self.neckRadius/self.segmentMag,-1*previousVec[0]*self.neckRadius/self.segmentMag)

        rightNextBodyPoint=(bodyVec[1]*self.neckRadius/self.segmentMag,-1*bodyVec[0]*self.neckRadius/self.segmentMag)
        leftNextBodyPoint=(-1*bodyVec[1]*self.neckRadius/self.segmentMag,bodyVec[0]*self.neckRadius/self.segmentMag)

        if bodyAngle>=0:
            #right
            point2R=(self.currentPoints[segmentNumber][0]+rightBodyPoint[0],self.currentPoints[segmentNumber][1]+rightBodyPoint[1])
            pg.draw.aaline(gameDisplay,(255,0,0),passPoints[1],point2R)
            
            point3R=(self.currentPoints[segmentNumber][0]+rightNextBodyPoint[0],self.currentPoints[segmentNumber][1]+rightNextBodyPoint[1])
            pg.draw.aaline(gameDisplay,(255,0,0),point2R,point3R)

            #left
            point3L=(self.currentPoints[segmentNumber][0]+leftNextBodyPoint[0],self.currentPoints[segmentNumber][1]+leftNextBodyPoint[1])
            pg.draw.aaline(gameDisplay,(255,0,0),passPoints[0],point3L)

            passPoints=(point3L,point3R)
            
        else:
            #right
            point3R=(self.currentPoints[segmentNumber][0]+rightBodyPoint[0],self.currentPoints[segmentNumber][1]+rightBodyPoint[1])
            pg.draw.aaline(gameDisplay,(255,0,0),passPoints[1],point3R)

            #left
            point2L=(self.currentPoints[segmentNumber][0]+leftBodyPoint[0],self.currentPoints[segmentNumber][1]+leftBodyPoint[1])
            pg.draw.aaline(gameDisplay,(255,0,0),passPoints[0],point2L)
            
            point3L=(self.currentPoints[segmentNumber][0]+leftNextBodyPoint[0],self.currentPoints[segmentNumber][1]+leftNextBodyPoint[1])
            pg.draw.aaline(gameDisplay,(255,0,0),point2L,point3L)

            passPoints=(point3L,point3R)

        previousVec=(-1*bodyVec[0],-1*bodyVec[1])

        return(previousVec,passPoints)


    def renderEye(self,other,headAngle):
        
        #eye rendering
        for i in range(0,self.eyeLen-1):
            point1X=self.eyeMags[i]*sin(headAngle+self.eyeAngles[i])+self.currentPoints[0][0]
            point1Y=self.eyeMags[i]*cos(headAngle+self.eyeAngles[i])+self.currentPoints[0][1]

            point2X=self.eyeMags[i+1]*sin(headAngle+self.eyeAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.eyeMags[i+1]*cos(headAngle+self.eyeAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,(255,0,0),(point1X,point1Y),(point2X,point2Y))

        point1X=self.eyeMags[0]*sin(headAngle+self.eyeAngles[0])+self.currentPoints[0][0]
        point1Y=self.eyeMags[0]*cos(headAngle+self.eyeAngles[0])+self.currentPoints[0][1]
        pg.draw.aaline(gameDisplay,(255,0,0),(point1X,point1Y),(point2X,point2Y))

        #iris rendering note, iris doesnt automatically connect back to the end
        
        for i in range(0,self.irisLen-1):
            point1X=self.irisMags[i]*sin(headAngle+self.irisAngles[i])+self.currentPoints[0][0]
            point1Y=self.irisMags[i]*cos(headAngle+self.irisAngles[i])+self.currentPoints[0][1]

            point2X=self.irisMags[i+1]*sin(headAngle+self.irisAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.irisMags[i+1]*cos(headAngle+self.irisAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,(255,0,0),(point1X,point1Y),(point2X,point2Y))
        
        point1X=self.irisMags[0]*sin(headAngle+self.irisAngles[0])+self.currentPoints[0][0]
        point1Y=self.irisMags[0]*cos(headAngle+self.irisAngles[0])+self.currentPoints[0][1]
        pg.draw.aaline(gameDisplay,(255,0,0),(point1X,point1Y),(point2X,point2Y))

        pupilDraw=[]
        for i in range(0,self.pupilLen-1):
            point1X=self.pupilMags[i]*sin(headAngle+self.pupilAngles[i])+self.currentPoints[0][0]
            point1Y=self.pupilMags[i]*cos(headAngle+self.pupilAngles[i])+self.currentPoints[0][1]

            
            point2X=self.pupilMags[i+1]*sin(headAngle+self.pupilAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.pupilMags[i+1]*cos(headAngle+self.pupilAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,(255,0,0),(point1X,point1Y),(point2X,point2Y))

        
    def renderStripe(self):
        for i in range(1,self.length-1):
            colorMod=255*i/(self.length-1)
            point1=self.currentPoints[i]
            point2=self.currentPoints[i+1]
            pg.draw.aaline(gameDisplay,(0,0,int(colorMod)),point1,point2)


    def renderSkin(self,other):

        #left and right are with head pointed upwards

        #first render head and eye seperatly
        headVec=(self.currentPoints[0][0]-self.currentPoints[1][0],self.currentPoints[0][1]-self.currentPoints[1][1])
        headAngle=-1*round(giveAngleSigned(headVec,(0,1)),config.round)
        self.renderEye(other,headAngle)
        self.renderStripe()

        for i in range(0,self.headSkinLen-1):
            point1X=self.headSkinMags[i]*sin(headAngle+self.headSkinAngles[i])+self.currentPoints[0][0]
            point1Y=self.headSkinMags[i]*cos(headAngle+self.headSkinAngles[i])+self.currentPoints[0][1]

            point2X=self.headSkinMags[i+1]*sin(headAngle+self.headSkinAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.headSkinMags[i+1]*cos(headAngle+self.headSkinAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,(255,0,0),(point1X,point1Y),(point2X,point2Y))



        neckVec=(self.currentPoints[2][0]-self.currentPoints[1][0],self.currentPoints[2][1]-self.currentPoints[1][1])
        
        neckAngle=round(giveAngleSigned(headVec,neckVec),config.round)

        rightNeckPoint=(neckVec[1]*self.neckRadius/self.segmentMag,-1*neckVec[0]*self.neckRadius/self.segmentMag)
        leftNeckPoint=(-1*neckVec[1]*self.neckRadius/self.segmentMag,neckVec[0]*self.neckRadius/self.segmentMag)

        if neckAngle<=0:
            point1X=self.headSkinMags[0]*sin(headAngle+self.headSkinAngles[0])+self.currentPoints[0][0]
            point1Y=self.headSkinMags[0]*cos(headAngle+self.headSkinAngles[0])+self.currentPoints[0][1]
            point1=(point1X,point1Y)

            point2X=self.currentPoints[1][0]+leftNeckPoint[0]
            point2Y=self.currentPoints[1][1]+leftNeckPoint[1]
            point2=(point2X,point2Y)
            pg.draw.aaline(gameDisplay,(255,0,0),point1,point2)

            #passPoints are ordered index 0 for left, 1 for right

            point3X=self.headSkinMags[-1]*sin(headAngle+self.headSkinAngles[-1])+self.currentPoints[0][0]
            point3Y=self.headSkinMags[-1]*cos(headAngle+self.headSkinAngles[-1])+self.currentPoints[0][1]
            point3=(point3X,point3Y)
            passPoints=(point2,point3)
        
        else:
            point1X=self.headSkinMags[-1]*sin(headAngle+self.headSkinAngles[-1])+self.currentPoints[0][0]
            point1Y=self.headSkinMags[-1]*cos(headAngle+self.headSkinAngles[-1])+self.currentPoints[0][1]
            point1=(point1X,point1Y)

            point2X=self.currentPoints[1][0]+rightNeckPoint[0]
            point2Y=self.currentPoints[1][1]+rightNeckPoint[1]

            point2=(point2X,point2Y)
            pg.draw.aaline(gameDisplay,(255,0,0),point1,point2)
        
            point3X=self.headSkinMags[0]*sin(headAngle+self.headSkinAngles[0])+self.currentPoints[0][0]
            point3Y=self.headSkinMags[0]*cos(headAngle+self.headSkinAngles[0])+self.currentPoints[0][1]
            point3=(point3X,point3Y)
            #passPoints are ordered index 0 for left, 1 for right
            passPoints=(point3,point2)



        previousVec=(-1*neckVec[0],-1*neckVec[1])
        #self.renderBodySegment(2,previousVec,passPoints)
        #then render body
        numberOfLoops=self.length-3
        for i in range(2,numberOfLoops+2):
            previousVec,passPoints=self.renderBodySegment(i,previousVec,passPoints)
            

        #then render tail
        pg.draw.aaline(gameDisplay,(255,0,0),passPoints[0],self.currentPoints[-1])
        pg.draw.aaline(gameDisplay,(255,0,0),passPoints[1],self.currentPoints[-1])


orbFactory=rb.OrbFactory()
orbFactory.initalizePools()

#snake inputs are as follows
#playerNumber,startingSpeed,turningRadius,startingLength,segmentLength,dashDistance
p1=Snake(1,3,70,5,20,100)
p1.createSnake(screenSize)

p2=Snake(2,3,70,5,20,100)
p2.createSnake(screenSize)

players=[p1,p2]
numberOfPlayers=len(players)
    
while not (p1.dead or p2.dead):
    #print(clock)
    tickNumber+=1
    playersHandler(players)
    rb.updateAndDisplayOrbs(orbFactory,players,gameDisplay,tickNumber)
    if tickNumber%gameLength==0:
        p1.dead=True
        p2.dead=True
    
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
    
    if p1.dead:
        print("player 1 died")
    
    if p2.dead:
        print("player 2 died")
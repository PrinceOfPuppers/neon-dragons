import pygame as pg
from math import sin,cos,pi,sqrt,acos
import numpy as np
from config import config
from orb import orbFactory,updateAndDisplayOrbs
from assets import stalkerAssets,watcherAssets
from random import random,uniform

def isPointOffScreeen(point,config):
    if 0>point[0] or point[0]>config.screenSize[0]:
        return(True)
    if 0>point[1] or point[1]>config.screenSize[1]:
        return(True)
    return(False)

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
    snake1Point1=snake1.currentPoints[0]
    snake1Point2=snake1.currentPoints[1]
    for i in range(0,snake2.length-1):
        snake2Point1=snake2.currentPoints[i]
        snake2Point2=snake2.currentPoints[i+1]
    
        if doLineSegmentsIntersect(snake1Point1,snake1Point2,snake2Point1,snake2Point2):
            #mutual eat
            if i==0:
                if snake1.sheildActive:
                    snake2.changeSnakeSize(1)
                elif snake2.sheildActive:
                    snake1.changeSnakeSize(1)
                else:
                    snake1.changeSnakeSize(1)
                    snake2.changeSnakeSize(1)
                return(True,True)
            
            #snake1 ate snake 2
            else:
                if snake2.sheildActive:
                    snake1.changeSnakeSize(1)
                else:
                    snake2.changeSnakeSize(i+1)
                return(True,False)
    return(False,False)

def dashEatCheck(snake1,snake2,prevPosition):
    #snake1 is dashing

    for i in range(0,snake2.length-1):
        snake2Point1=snake2.currentPoints[i]
        snake2Point2=snake2.currentPoints[i+1]
    
        if doLineSegmentsIntersect(prevPosition,snake1.position,snake2Point1,snake2Point2):
            #mutual eat
            if i==0:
                if snake1.sheildActive:
                    snake2.changeSnakeSize(1)
                elif snake2.sheildActive:
                    snake1.changeSnakeSize(1)
                else:
                    snake1.changeSnakeSize(1)
                    snake2.changeSnakeSize(1)
                return(True,True)
            
            #snake1 ate snake 2
            else:
                if snake2.sheildActive:
                    snake1.changeSnakeSize(1)
                else:
                    snake2.changeSnakeSize(i+1)
                return(True,False)
    return(False,False)



def didSnakeEatSelf(snake):
    headPoint1=snake.currentPoints[0]
    headPoint2=snake.currentPoints[1]
    for i in range(2,snake.length-1):
        snakePoint1=snake.currentPoints[i]
        snakePoint2=snake.currentPoints[i+1]
    
        if doLineSegmentsIntersect(headPoint1,headPoint2,snakePoint1,snakePoint2):
            if snake.sheildActive:
                snake.changeSnakeSize(1)
            else:
                snake.changeSnakeSize(i+1)
            return(True)
    return(False)

def applyControls(p1,p2,keys,gameDisplay,tickNumber):
    #keys is a list of bools, layed out as follows (w,a,s,d,up,left,down,right)
    for event in pg.event.get():
        # checks if player has quit
        if event.type == pg.QUIT:
            config.quit=True


    #p1 controls
    if keys[1]:
        p1.rot+=p1.rotVel
    if keys[3]:
        p1.rot-=p1.rotVel
    #p1 dash
    if keys[0]:
        p1.dash(p2,gameDisplay,tickNumber)
    #p1 shield
    if keys[2]:
        p1.sheild(tickNumber)

    #p2 controls
    if keys[5]:
        p2.rot+=p2.rotVel
    if keys[7]:
        p2.rot-=p2.rotVel
    #p2 dash
    if keys[4]:
        p2.dash(p1,gameDisplay,tickNumber)
    #p2 shield
    if keys[6]:
        p2.sheild(tickNumber)

def playersHandler(p1,p2,keys,gameDisplay,tickNumber):
    #applys all player operations for a single tick
    p1.updateAndDisplay(p2,gameDisplay,tickNumber)
    p2.updateAndDisplay(p1,gameDisplay,tickNumber)
    applyControls(p1,p2,keys,gameDisplay,tickNumber)

def modDistance(val1,val2,mod):
    diff1=abs((val1-val2)%mod)
    diff2=abs((val2-val1)%mod)

    if diff1<diff2:
        return(diff1)
    return(diff2)

def dashEatOrbCheck(orbFactory,player,prevPosition):
    for orb in orbFactory.activeStaticSizeChangeOrbs:
        orbcorner1=(orb.position[0]-orb.halfBoxWidth,orb.position[1]-orb.halfBoxWidth)
        orbcorner2=(orb.position[0]-orb.halfBoxWidth,orb.position[1]+orb.halfBoxWidth)
        orbcorner3=(orb.position[0]+orb.halfBoxWidth,orb.position[1]-orb.halfBoxWidth)
        orbcorner4=(orb.position[0]+orb.halfBoxWidth,orb.position[1]+orb.halfBoxWidth)

        if doLineSegmentsIntersect(prevPosition,player.position,orbcorner1,orbcorner2):
                player.changeSnakeSize(player.length+orb.sizeChange)
                orbFactory.deactivateOrb(orb)
                
        elif doLineSegmentsIntersect(prevPosition,player.position,orbcorner2,orbcorner3):
                player.changeSnakeSize(player.length+orb.sizeChange)
                orbFactory.deactivateOrb(orb)

        elif doLineSegmentsIntersect(prevPosition,player.position,orbcorner3,orbcorner4):
                player.changeSnakeSize(player.length+orb.sizeChange)
                orbFactory.deactivateOrb(orb)

        elif doLineSegmentsIntersect(prevPosition,player.position,orbcorner4,orbcorner1):
                player.changeSnakeSize(player.length+orb.sizeChange)
                orbFactory.deactivateOrb(orb)

class Snake:
    #the snake consists of a number of segments who follow the previous path of the head of the snake, the segment length just determines how many ticks ago they follow
    #the position of the snake each tick are recorded each tick to a list, the length of which is dynamically increased depending on how long the snake is
    def __init__(self,playerNumber,startingSpeed,turningRadius,segmentLength,dashDistance):
        #length refers to number of segments
        self.dead=False
        self.playerNumber=playerNumber    
        self.position=[0,0]
        self.rot=0
        self.turningRadius=turningRadius
        self.rotVel=startingSpeed/turningRadius
        self.speed=startingSpeed

        #sheild cooldown is mesured from when its first activated
        self.sheildActive=False
        self.lastSheilded=-config.sheildCoolDown
        self.sheildDuration=config.sheildDuration
        self.sheildCooldown=config.sheildCoolDown

        #segment length is the number of ticks long it is, it will change with speed
        self.segmentLength=segmentLength
        self.dashDistance=dashDistance
        self.lastTickDashed=-100
        self.dashCoolDown=100
        #these are all updated in create snake
        #the list oldest entry in the list is updated, so the poisistion of the head must be recorded and is incremeted each tick
        #this way only one element of the list must be changed each tick, a list is used becasuse we will have to increase the size
        #as parameters of the snake are changed (ie length)
        self.previousPositions=[]
        self.length=0
        self.positionListLength=0
        self.headIndexInPositionList=0
        self.color=(255,255,255)
        #list of points currently in the snake (index zero will always be head)
        self.currentPoints=[]
        self.segmentMag=segmentLength*startingSpeed



    def createSnake(self,length,turningRadius):
        #resetsSnake
        self.lastTickDashed=-100
        self.dead=False
        self.changeTurningRadius(turningRadius)
        self.position=[0,0]
        self.rot=0
        self.previousPositions=[]
        self.currentPoints=[]
        self.length=length
        
        self.sheildActive=False
        self.lastSheilded=-config.sheildCoolDown
        #generates a list for recording the previous positions 
        self.positionListLength=(self.length-1)*self.segmentLength+1
        self.headIndexInPositionList=self.positionListLength-1

        for i in range(0,self.positionListLength):
            if self.playerNumber==1:
                self.rot=pi
                self.position=[config.screenSize[0]/2+self.turningRadius,config.screenSize[1]/2]
                positionOfHeadPreviously=[self.position[0],self.position[1]+(self.positionListLength-i)*self.speed]
                self.previousPositions.append(positionOfHeadPreviously)
            
            if self.playerNumber==2:
                
                self.position=[config.screenSize[0]/2-self.turningRadius,config.screenSize[1]/2]
                positionOfHeadPreviously=[self.position[0],self.position[1]-(self.positionListLength-i)*self.speed]
                self.previousPositions.append(positionOfHeadPreviously)

        for i in range(0,self.length):
            self.currentPoints.append([0,0])
        
        self.grabAssets()
        
    def changeTurningRadius(self,turningRadius):
        self.turningRadius=turningRadius
        self.rotVel=self.speed/turningRadius
    
    def grabAssets(self):
        if self.playerNumber==1:
            self.transformaitonLengths=config.transformationLengths
            self.styleType=1
            for i in range(0,len(self.transformaitonLengths)):
                if self.length>=self.transformaitonLengths[i]:
                    self.styleType=i+2
            #fits head to any segmentlength/speed combo
            self.headSkin,self.neckRadius=stalkerAssets.scaleHead(self)
            self.headSkinMags=[]
            self.headSkinAngles=[]
            self.headSkinLen=len(self.headSkin)
            self.eye,self.iris,self.pupil=stalkerAssets.scaleEye(self)
        
        elif self.playerNumber==2:
            self.transformaitonLengths=config.transformationLengths
            self.styleType=1
            for i in range(0,len(self.transformaitonLengths)):
                if self.length>=self.transformaitonLengths[i]:
                    self.styleType=i+2
            #fits head to any segmentlength/speed combo
            self.headSkin,self.neckRadius=watcherAssets.scaleHead(self)
            self.headSkinMags=[]
            self.headSkinAngles=[]
            self.headSkinLen=len(self.headSkin)

            self.eye,self.iris,self.pupil=watcherAssets.scaleEye(self)

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

    def changeSnakeSize(self,newSize):
        sizeDifference=newSize-self.length
        self.length=newSize
        #removes entries from position list and updates the index of the head in the list
        if sizeDifference<=0:
            #removes elements from current points (points that are being displayed)
            del self.currentPoints[newSize:]

            previousPositionListLen=self.positionListLength
            numberOfEntriesToRemove=(-1*self.segmentLength*sizeDifference)
            
            if numberOfEntriesToRemove+self.headIndexInPositionList<previousPositionListLen:

                upperIndexToDelete=self.headIndexInPositionList+numberOfEntriesToRemove
                deleteTotal=abs(self.headIndexInPositionList+1 -1*(upperIndexToDelete+1))
                del self.previousPositions[self.headIndexInPositionList+1 : upperIndexToDelete+1]



            else:
                
                del self.previousPositions[self.headIndexInPositionList+1:previousPositionListLen]

                upperIndexToDelete=(self.headIndexInPositionList+numberOfEntriesToRemove)%previousPositionListLen
                deleteTotal=abs(self.headIndexInPositionList+1-previousPositionListLen)+abs(upperIndexToDelete+1)
                del self.previousPositions[0:upperIndexToDelete+1]

                self.headIndexInPositionList-=(self.headIndexInPositionList+numberOfEntriesToRemove+1)%previousPositionListLen

                for i in range(0,sizeDifference):
                    self.currentPoints.append([0,0])
                
            
            self.positionListLength=len(self.previousPositions)
            
            if not self.positionListLength==self.segmentLength*(self.length-1)+1:
                print("decreaseLength error!")
        
        else:
            #adds dummy data to current point list, they will have the correct info added in update and d
            for i in range(0,sizeDifference):
                self.currentPoints.append([0,0])

            previousPositionListLen=self.positionListLength
            numberOfEntriesToAdd=(self.segmentLength*sizeDifference)
            headIndex=self.headIndexInPositionList
            
            tailIndex=(headIndex+1)%previousPositionListLen
            tailPosition=self.previousPositions[tailIndex]
            if tailIndex==0:
                self.headIndexInPositionList+=numberOfEntriesToAdd

            for i in range(0,numberOfEntriesToAdd):
                point=[tailPosition[0],tailPosition[1]]
                self.previousPositions.insert(tailIndex,point)
            
            self.positionListLength=len(self.previousPositions)
            if not self.positionListLength==self.segmentLength*(self.length-1)+1:
                print("increaseLength error!")
        
        if self.length<=2:
            self.dead=True

        #checks if style of snake needs to be changed
        styleType=1
        for i in range(0,len(self.transformaitonLengths)):
            if self.length>=self.transformaitonLengths[i]:
                styleType=i+2
        
        if styleType!=self.styleType:
            self.styleType=styleType
            self.grabAssets()

        
    def _applyAndRecordTickMotion(self):
        self.position[0] += self.speed*sin(self.rot)
        self.position[1] += self.speed*cos(self.rot)

        self.headIndexInPositionList+=1
        self.headIndexInPositionList=self.headIndexInPositionList%self.positionListLength

        self.previousPositions[self.headIndexInPositionList][0]=self.position[0]
        self.previousPositions[self.headIndexInPositionList][1]=self.position[1]


    def dash(self,other,gameDisplay,tickNumber):

        longEnoughToDash=self.length>=self.transformaitonLengths[0]
        dashOffCooldown=tickNumber-self.lastTickDashed>=self.dashCoolDown

        if dashOffCooldown and longEnoughToDash:
            prevPosition=(self.position[0],self.position[1])

            for i in range(0,self.dashDistance):
                didSnakeEatSelf(self)
                if self.dead:
                    break
                #stripped down update and display for dashing
                self._applyAndRecordTickMotion()
                for i in range(0,self.length):
                    segmentPositionIndex=(self.headIndexInPositionList-i*self.segmentLength)%self.positionListLength
                    segmentPosition=self.previousPositions[segmentPositionIndex]
                    self.currentPoints[i][0]=segmentPosition[0]
                    self.currentPoints[i][1]=segmentPosition[1]
                self.renderSkin(gameDisplay,tickNumber)
            
            self.lastTickDashed=tickNumber
            #specialized collision detection to improve dash preformance
            dashEatCheck(self,other,prevPosition)
            dashEatOrbCheck(orbFactory,self,prevPosition)
            pg.display.update()

    def sheild(self,tickNumber):
        longEnoughToSheild=self.length>=self.transformaitonLengths[1]
        sheildOffCoolDown=tickNumber-self.lastSheilded>self.sheildCooldown

        if longEnoughToSheild and sheildOffCoolDown:
            self.sheildActive=True
            self.lastSheilded=tickNumber


    def updateAndDisplay(self,other,gameDisplay,tickNumber):
        self._applyAndRecordTickMotion()

        for i in range(0,self.length):
            
            segmentPositionIndex=(self.headIndexInPositionList-i*self.segmentLength)%self.positionListLength
            segmentPosition=self.previousPositions[segmentPositionIndex]
            self.currentPoints[i][0]=segmentPosition[0]
            self.currentPoints[i][1]=segmentPosition[1]

        #checks self intersection and renders skin
        if self.length>2:

            self.renderSkin(gameDisplay,tickNumber)
        
            #checks eating other
            if other.length>2:
                didEatOtherSnake(self,other) 

            #turns off sheild after its duration runs out
            if self.sheildActive:
                if tickNumber-self.lastSheilded>self.sheildDuration:
                    self.sheildActive=False  

            didSnakeEatSelf(self)

        #checks if either player is offscreen
        if isPointOffScreeen(self.position,config):
            self.dead=True
        if isPointOffScreeen(other.position,config):
            other.dead=True
        
    #render eye,render stripe and render body segment are all controled by render skin
    def renderBodySegment(self,gameDisplay,segmentNumber,previousVec,passPoints,color):
        bodyVec=(self.currentPoints[segmentNumber+1][0]-self.currentPoints[segmentNumber][0],self.currentPoints[segmentNumber+1][1]-self.currentPoints[segmentNumber][1])
        bodyAngle=round(giveAngleSigned(previousVec,bodyVec),config.round)
        
        
        rightBodyPoint=(-1*previousVec[1]*self.neckRadius/self.segmentMag,previousVec[0]*self.neckRadius/self.segmentMag)
        leftBodyPoint=(previousVec[1]*self.neckRadius/self.segmentMag,-1*previousVec[0]*self.neckRadius/self.segmentMag)

        rightNextBodyPoint=(bodyVec[1]*self.neckRadius/self.segmentMag,-1*bodyVec[0]*self.neckRadius/self.segmentMag)
        leftNextBodyPoint=(-1*bodyVec[1]*self.neckRadius/self.segmentMag,bodyVec[0]*self.neckRadius/self.segmentMag)

        if bodyAngle>=0:
            #right
            point2R=(self.currentPoints[segmentNumber][0]+rightBodyPoint[0],self.currentPoints[segmentNumber][1]+rightBodyPoint[1])
            pg.draw.aaline(gameDisplay,color,passPoints[1],point2R)
            
            point3R=(self.currentPoints[segmentNumber][0]+rightNextBodyPoint[0],self.currentPoints[segmentNumber][1]+rightNextBodyPoint[1])
            pg.draw.aaline(gameDisplay,color,point2R,point3R)

            #left
            point3L=(self.currentPoints[segmentNumber][0]+leftNextBodyPoint[0],self.currentPoints[segmentNumber][1]+leftNextBodyPoint[1])
            pg.draw.aaline(gameDisplay,color,passPoints[0],point3L)

            passPoints=(point3L,point3R)
            
        else:
            #right
            point3R=(self.currentPoints[segmentNumber][0]+rightBodyPoint[0],self.currentPoints[segmentNumber][1]+rightBodyPoint[1])
            pg.draw.aaline(gameDisplay,color,passPoints[1],point3R)

            #left
            point2L=(self.currentPoints[segmentNumber][0]+leftBodyPoint[0],self.currentPoints[segmentNumber][1]+leftBodyPoint[1])
            pg.draw.aaline(gameDisplay,color,passPoints[0],point2L)
            
            point3L=(self.currentPoints[segmentNumber][0]+leftNextBodyPoint[0],self.currentPoints[segmentNumber][1]+leftNextBodyPoint[1])
            pg.draw.aaline(gameDisplay,color,point2L,point3L)

            passPoints=(point3L,point3R)

        previousVec=(-1*bodyVec[0],-1*bodyVec[1])

        return(previousVec,passPoints)


    def renderEye(self,gameDisplay,headAngle):
        if self.sheildActive:
            color=(255,255,255)
        else:
            color=self.color
        #eye rendering
        for i in range(0,self.eyeLen-1):
            point1X=self.eyeMags[i]*sin(headAngle+self.eyeAngles[i])+self.currentPoints[0][0]
            point1Y=self.eyeMags[i]*cos(headAngle+self.eyeAngles[i])+self.currentPoints[0][1]

            point2X=self.eyeMags[i+1]*sin(headAngle+self.eyeAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.eyeMags[i+1]*cos(headAngle+self.eyeAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,color,(point1X,point1Y),(point2X,point2Y))

        point1X=self.eyeMags[0]*sin(headAngle+self.eyeAngles[0])+self.currentPoints[0][0]
        point1Y=self.eyeMags[0]*cos(headAngle+self.eyeAngles[0])+self.currentPoints[0][1]
        pg.draw.aaline(gameDisplay,color,(point1X,point1Y),(point2X,point2Y))

        #iris rendering note, iris doesnt automatically connect back to the end
        
        for i in range(0,self.irisLen-1):
            point1X=self.irisMags[i]*sin(headAngle+self.irisAngles[i])+self.currentPoints[0][0]
            point1Y=self.irisMags[i]*cos(headAngle+self.irisAngles[i])+self.currentPoints[0][1]

            point2X=self.irisMags[i+1]*sin(headAngle+self.irisAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.irisMags[i+1]*cos(headAngle+self.irisAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,color,(point1X,point1Y),(point2X,point2Y))
        
        point1X=self.irisMags[0]*sin(headAngle+self.irisAngles[0])+self.currentPoints[0][0]
        point1Y=self.irisMags[0]*cos(headAngle+self.irisAngles[0])+self.currentPoints[0][1]
        pg.draw.aaline(gameDisplay,color,(point1X,point1Y),(point2X,point2Y))

        for i in range(0,self.pupilLen-1):
            point1X=self.pupilMags[i]*sin(headAngle+self.pupilAngles[i])+self.currentPoints[0][0]
            point1Y=self.pupilMags[i]*cos(headAngle+self.pupilAngles[i])+self.currentPoints[0][1]

            
            point2X=self.pupilMags[i+1]*sin(headAngle+self.pupilAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.pupilMags[i+1]*cos(headAngle+self.pupilAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,color,(point1X,point1Y),(point2X,point2Y))

        
    def renderStripe(self,gameDisplay):
        for i in range(1,self.length-1):
            colorMod=255*i/(self.length-1)
            point1=self.currentPoints[i]
            point2=self.currentPoints[i+1]
            pg.draw.aaline(gameDisplay,(0,0,int(colorMod)),point1,point2)


    def renderSkin(self,gameDisplay,tickNumber):

        #head color
        if self.sheildActive:
            mod=(self.segmentLength*self.length)
            maxModDist=mod/2
            colorWrapping=tickNumber%mod
            colorMod=modDistance(colorWrapping,0,mod)/maxModDist
            color=(255*colorMod,255*colorMod,255)
        else:
            color=self.color
        #left and right are with head pointed upwards

        #first render head and eye seperatly
        headVec=(self.currentPoints[0][0]-self.currentPoints[1][0],self.currentPoints[0][1]-self.currentPoints[1][1])
        headAngle=-1*round(giveAngleSigned(headVec,(0,1)),config.round)
        self.renderEye(gameDisplay,headAngle)
        self.renderStripe(gameDisplay)

        for i in range(0,self.headSkinLen-1):
            point1X=self.headSkinMags[i]*sin(headAngle+self.headSkinAngles[i])+self.currentPoints[0][0]
            point1Y=self.headSkinMags[i]*cos(headAngle+self.headSkinAngles[i])+self.currentPoints[0][1]

            point2X=self.headSkinMags[i+1]*sin(headAngle+self.headSkinAngles[i+1])+self.currentPoints[0][0]
            point2Y=self.headSkinMags[i+1]*cos(headAngle+self.headSkinAngles[i+1])+self.currentPoints[0][1]
            pg.draw.aaline(gameDisplay,color,(point1X,point1Y),(point2X,point2Y))



        neckVec=(self.currentPoints[2][0]-self.currentPoints[1][0],self.currentPoints[2][1]-self.currentPoints[1][1])
        
        neckAngle=round(giveAngleSigned(headVec,neckVec),config.round)

        rightNeckPoint=(neckVec[1]*self.neckRadius/self.segmentMag,-1*neckVec[0]*self.neckRadius/self.segmentMag)
        leftNeckPoint=(-1*neckVec[1]*self.neckRadius/self.segmentMag,neckVec[0]*self.neckRadius/self.segmentMag)

        #neck color
        if self.sheildActive:
            colorMod=modDistance(colorWrapping,self.segmentLength,mod)/maxModDist
            color=(255*colorMod,255*colorMod,255)

        else:
            color=self.color
        
        if neckAngle<=0:
            point1X=self.headSkinMags[0]*sin(headAngle+self.headSkinAngles[0])+self.currentPoints[0][0]
            point1Y=self.headSkinMags[0]*cos(headAngle+self.headSkinAngles[0])+self.currentPoints[0][1]
            point1=(point1X,point1Y)

            point2X=self.currentPoints[1][0]+leftNeckPoint[0]
            point2Y=self.currentPoints[1][1]+leftNeckPoint[1]
            point2=(point2X,point2Y)
            pg.draw.aaline(gameDisplay,color,point1,point2)

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
            pg.draw.aaline(gameDisplay,color,point1,point2)
        
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
            if self.sheildActive:
                colorMod=modDistance(colorWrapping,i*self.segmentLength,mod)/maxModDist
                color=(255*colorMod,255*colorMod,255)
            else:
                color=self.color
            previousVec,passPoints=self.renderBodySegment(gameDisplay,i,previousVec,passPoints,color)
            

        #then render tail
        if self.sheildActive:
            colorMod=modDistance(colorWrapping,self.length*self.segmentLength,mod)/maxModDist
            color=(255*colorMod,255*colorMod,255)
        else:
            color=self.color
        pg.draw.aaline(gameDisplay,color,passPoints[0],self.currentPoints[-1])
        pg.draw.aaline(gameDisplay,color,passPoints[1],self.currentPoints[-1])
from random import random,uniform
from config import config
import pygame as pg
from math import sin,cos,pi
from assets import orbAssets

#when implementing new orbs:

#give them new type
#increase orbTypesImplemented in factory
#add both active and inactive lists
#add both lists to initalize pools method
#add to deactivate orbs method
#add to orbs spawn handler
#add to update and display orbs funciton
#add orb to reset pools





def isPointInSquare(pointX,pointY,squareX,squareY,halfSquareWidth):
    if (pointX>=(squareX-halfSquareWidth)) and (pointX<=(squareX+halfSquareWidth)):
        if (pointY>=(squareY-halfSquareWidth)) and (pointY<=(squareY+halfSquareWidth)):
            return(True)
    return(False)

def isSpawnLocationOccupied(spawnLocationX,spawnLocationY,players):
    for player in players:
        pointX=player.position[0]
        pointY=player.position[1]
    
        halfSquareWidth=config.halfOrbHitbox+config.orbSpawnBuffer
        if isPointInSquare(pointX,pointY,spawnLocationX,spawnLocationY,halfSquareWidth):
            return(True)
    return(False)

def updateAndDisplayOrbs(orbFactory,players,gameDisplay,tickNumber):

    for orb in orbFactory.activeStaticSizeChangeOrbs:
        #displays main lines
        for line in orb.lines:
            point1=(round(orb.position[0]+line[0][0],config.round),round(orb.position[1]+line[0][1],config.round))
            point2=(round(orb.position[0]+line[1][0],config.round),round(orb.position[1]+line[1][1],config.round))
            pg.draw.aaline(gameDisplay,orb.color,point1,point2)
        #check if eaten
        for player in players:
            if orb.wasOrbEaten(player):
                print("pre eat size:",player.length)
                player.changeSnakeSize(player.length+orb.sizeChange)
                orbFactory.deactivateOrb(orb)
                
                print("orb eaten,sizechange:",orb.sizeChange)
                print("snakeSize:",player.length)

    for orb in orbFactory.activeMovingSizeChangeOrbs:
        orb.wander(tickNumber)

        #displays main lines
        for line in orb.lines:
            point1=(round(orb.position[0]+line[0][0],config.round),round(orb.position[1]+line[0][1],config.round))
            point2=(round(orb.position[0]+line[1][0],config.round),round(orb.position[1]+line[1][1],config.round))
            pg.draw.aaline(gameDisplay,orb.color,point1,point2)
        
        #check if eaten
        for player in players:
            if orb.wasOrbEaten(player):
                print("pre eat size:",player.length)
                player.changeSnakeSize(player.length+orb.sizeChange)
                orbFactory.deactivateOrb(orb)
                print("orb eaten,sizechange:",orb.sizeChange)
                print("snakeSize:",player.length)



class OrbFactory:
    def __init__(self,orbPoolSize=5):

        
        self.orbPoolSize=orbPoolSize
        #note on type, first index is non moving (0) or moving (1)
        #second number denotes effect ie 0 is size change

        #this number denotes the max value of the second number in 
        #the type ordered pair
        self.orbTypesImplemented=0

        #inactiveLists
        #type (0,0)
        self.inactiveStaticSizeChangeOrbs=[]
        #type (1,0)
        self.inactiveMovingSizeChangeOrbs=[]


        #activeLists
        #type (0,0)
        self.activeStaticSizeChangeOrbs=[]
        #type (1,0)
        self.activeMovingSizeChangeOrbs=[]
    
    def initalizePools(self):
        for i in range(0,self.orbPoolSize):
            staticSizeChangeOrb=StaticSizeChangeOrb()
            movingSizeChangeOrb=MovingSizeChangeOrb()

            self.inactiveStaticSizeChangeOrbs.append(staticSizeChangeOrb)
            self.inactiveMovingSizeChangeOrbs.append(movingSizeChangeOrb)

    def spawnHandler(self,tickNumber,players):
        print(len(self.activeStaticSizeChangeOrbs))
        print(len(self.activeMovingSizeChangeOrbs))
        #spawn static orb
        if tickNumber%config.staticOrbSpawnPeriod==0:
            
            orbType=round(uniform(0,self.orbTypesImplemented))
            spawnType=orbType
            #sizeChangeOrb
            if spawnType==0:
                #checks if inactive pool has any avalible
                if not len(self.inactiveStaticSizeChangeOrbs)==0:

                    spawnLocationX=random()*config.screenSize[0]
                    spawnLocaitonY=random()*config.screenSize[1]
                    #checks if spawn locaiton is too close to player head
                    spawnLocationIsOccupied=isSpawnLocationOccupied(spawnLocationX,spawnLocaitonY,players)
                    
                    sizeChange=round(uniform(-1*config.sizeChangeOrbRange,config.sizeChangeOrbRange)+config.sizeChangeOrbPositiveBias)

                    #all chekcs passed, spawning orb
                    if not (spawnLocationIsOccupied or sizeChange==0):
                        orb=self.inactiveStaticSizeChangeOrbs.pop(0)
                        orb.position[0]=spawnLocationX
                        orb.position[1]=spawnLocaitonY
                        orb.sizeChange=sizeChange
                        

                        if sizeChange<0:
                            colorMod=int(round(abs(255*sizeChange)/(2*config.sizeChangeOrbRange -config.sizeChangeOrbPositiveBias)))
                            orb.color=(255,255-colorMod,255-colorMod)
                        else:
                            colorMod=int(round(abs(255*sizeChange)/(2*config.sizeChangeOrbRange +config.sizeChangeOrbPositiveBias)))
                            orb.color=(255-colorMod,255,255-colorMod)

                        print("StaticSizeChangeOrbSpawned")
                        self.activeStaticSizeChangeOrbs.append(orb)


        #spawn moving orb
        if tickNumber%config.movingOrbSpawnPeriod==0:

            orbType=round(uniform(0,self.orbTypesImplemented))
            spawnType=orbType

            #sizeChangeOrb
            if spawnType==0:
                #checks if inactive pool has any avalible
                if not len(self.inactiveMovingSizeChangeOrbs)==0:

                    spawnLocationX=random()*config.screenSize[0]
                    spawnLocaitonY=random()*config.screenSize[1]
                    #checks if spawn locaiton is too close to player head
                    spawnLocationIsOccupied=isSpawnLocationOccupied(spawnLocationX,spawnLocaitonY,players)
                    
                    sizeChange=round(uniform(-1*config.sizeChangeOrbRange,config.sizeChangeOrbRange)+config.sizeChangeOrbPositiveBias)

                    #all chekcs passed, spawning orb
                    if not (spawnLocationIsOccupied or sizeChange==0):
                        orb=self.inactiveMovingSizeChangeOrbs.pop(0)
                        orb.position[0]=spawnLocationX
                        orb.position[1]=spawnLocaitonY
                        orb.sizeChange=sizeChange
                        

                        if sizeChange<0:
                            colorMod=int(round(abs(255*sizeChange)/(2*config.sizeChangeOrbRange -config.sizeChangeOrbPositiveBias)))
                            orb.color=(255,255-colorMod,255-colorMod)
                        else:
                            colorMod=int(round(abs(255*sizeChange)/(2*config.sizeChangeOrbRange +config.sizeChangeOrbPositiveBias)))
                            orb.color=(255-colorMod,255,255-colorMod)

                        self.activeMovingSizeChangeOrbs.append(orb)
                        print("movingSizeChangeOrbSpawned")

    def deactivateOrb(self,orb):
        if orb.type==(0,0):
            self.activeStaticSizeChangeOrbs.remove(orb)
            self.inactiveStaticSizeChangeOrbs.append(orb)
        
        elif orb.type==(1,0):
            self.activeMovingSizeChangeOrbs.remove(orb)
            self.inactiveMovingSizeChangeOrbs.append(orb)

    def resetPools(self):
        for orb in self.activeStaticSizeChangeOrbs:
            self.deactivateOrb(orb)
        
        for orb in self.activeMovingSizeChangeOrbs:
            self.deactivateOrb(orb)



class _Orb:
    def __init__(self,startLocationX,startLocationY):
        self.position=[startLocationX,startLocationY]
        #collision box is 10 by 10, kept as a half because the full width is never used
        self.halfBoxWidth=config.halfOrbHitbox
        self.color=(255,255,255)

    #orb gets eaten if the snakes head is in its bounding box
    def wasOrbEaten(self,snake):
        headX=snake.position[0]
        headY=snake.position[1]

        orbX=self.position[0]
        orbY=self.position[1]
        halfBoxWidth=self.halfBoxWidth

        return(isPointInSquare(headX,headY,orbX,orbY,halfBoxWidth))
        
        

class _MovingOrb(_Orb):
    def __init__(self,startLocationX,startLocationY,erraticness,thrust,mass):
        super().__init__(startLocationX,startLocationY)
        self.erraticness=erraticness
        self.mass=mass
        self.velx=0
        self.vely=0
        self.lastWandered=0
        self.thrust=thrust
        #generates a bunch of random frequencies to add togeather to simulate smooth random motion
        self.periodicFreqx = self.randomFreq(erraticness)
        self.periodicFreqy = self.randomFreq(erraticness)
        
    def wander(self, tickNumber):
        # framerate Saving
        
        if (tickNumber-self.lastWandered)>0:
            self.lastWandered=tickNumber
            if tickNumber%4==0:
                
                self.velx += ((4*self.harmonicSinusoid(self.periodicFreqx,tickNumber) * (self.thrust))-12* self.velx**3) / self.mass
                self.vely += ((4*self.harmonicSinusoid(self.periodicFreqy,tickNumber) * (self.thrust))-12* self.vely**3) / self.mass

            self.position[0]+=self.velx
            self.position[1]+=self.vely

            self.position[0]=self.position[0]%config.screenSize[0]
            self.position[1]=self.position[1]%config.screenSize[1]
    
    @staticmethod
    def randomFreq(numbSinusoids):
        freqList = []
        while len(freqList) < numbSinusoids:
            freqList.append((random() - 1 / 2) / 50)
        return (freqList)

    # controls behavior of AI wandering,smooth periodic RNG
    @staticmethod
    def harmonicSinusoid(freqList, tickNumber):
        valueAtCurrentTick = 0
        for freq in freqList:
            valueAtCurrentTick += sin(freq * tickNumber)
        valueAtCurrentTick = valueAtCurrentTick / len(freqList)
        return (valueAtCurrentTick)

class _StaticOrb(_Orb):
    def __init__(self,startLocationX,startLocationY):
        super().__init__(startLocationX,startLocationY)


#size changing orbs
class StaticSizeChangeOrb(_StaticOrb):
    def __init__(self,startLocationX=-1,startLocationY=-1,sizeChange=0):

        super().__init__(startLocationX,startLocationY)
        self.lines=orbAssets.scaleAndTranslateStaticSizeChangeOrb(2*config.halfOrbHitbox)
        self.pointsLen=len(self.lines)
        self.sizeChange=sizeChange
        self.type=(0,0)

class MovingSizeChangeOrb(_MovingOrb):

    def __init__(self,startLocationX=-1,startLocationY=-1,sizeChange=0,erraticness=2,thrust=10,mass=100):
        super().__init__(startLocationX,startLocationY,erraticness,thrust,mass)
        self.lines=orbAssets.scaleAndTranslateMovingSizeChangeOrb(2*config.halfOrbHitbox)
        self.pointsLen=len(self.lines)
        self.sizeChange=sizeChange
        self.type=(1,0)


#speed changing orbs



orbFactory=OrbFactory()





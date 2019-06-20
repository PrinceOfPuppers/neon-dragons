import pygame as pg
class Button:
    def __init__(self,center,width,height,symbols,color,displaySquare):
        self.center=center
        self.posistion=(round(self.center[0]-width/2),round(self.center[1]-height/2))
        self.width=width
        self.height=height
        self.displaySquare=displaySquare
        for symbol in symbols:
            for point in symbol:
                point[0]+=center[0]
                point[1]+=center[1]
        self.symbols=symbols

        self.widthChangeOnHover=50
        self.heightChangeOnHover=50

        self.color=color
        self.points=[(self.posistion[0],self.posistion[1]),(self.posistion[0]+width,self.posistion[1]),(self.posistion[0]+width,self.posistion[1]+height),(self.posistion[0],self.posistion[1]+height)]
        self.wasPressed=False

    def displayAndGetClicked(self,mousePos,mousePressed,gameDisplay):
        self.wasPressed=False
        mouseIsOnButton=False
        if mousePos[0]>self.posistion[0] and mousePos[0]<(self.posistion[0]+self.width):
            if mousePos[1]>self.posistion[1] and mousePos[1]<(self.posistion[1]+self.height):
                mouseIsOnButton=True

        #square display
        if self.displaySquare:
            if mouseIsOnButton:
                color=(255,0,0)
                width=self.width+self.widthChangeOnHover
                height=self.height+self.heightChangeOnHover
                points=[(self.center[0]-width/2,self.center[1]-height/2),(self.center[0]-width/2,self.center[1]+height/2),(self.center[0]+width/2,self.center[1]+height/2),(self.center[0]+width/2,self.center[1]-height/2)]
                pg.draw.aalines(gameDisplay,color,True,points)

            else:
                pg.draw.aalines(gameDisplay,self.color,True,self.points)
        
        #symbols display
        if mouseIsOnButton:
            for symbol in self.symbols:
                    pg.draw.aalines(gameDisplay,color,True,symbol)
        else:
            for symbol in self.symbols:
                pg.draw.aalines(gameDisplay,self.color,True,symbol)

        
        if mouseIsOnButton and mousePressed[0]:
            self.wasPressed=True
        return(mouseIsOnButton)

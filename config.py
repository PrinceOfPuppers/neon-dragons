import tkinter
root=tkinter.Tk()

def scaleToResolution(screenSize):
    devWidth=1500
    userWidth=screenSize[0]
    widthRatio=userWidth/devWidth

    #the constant number in each is the desired value when screen width is 1500
    normalTurningRadius=int(round(70*widthRatio))

    menuTurningRadius=int(round(100*widthRatio))

    halfOrbHitBox=int(round(25*widthRatio))
    snakeSpeed=3*widthRatio

    movingOrbThrust=10*widthRatio
    textCharacterWidth=int(round(50*widthRatio))

    return(halfOrbHitBox,normalTurningRadius,menuTurningRadius,snakeSpeed,movingOrbThrust,textCharacterWidth)




class Config:

    def __init__(self):
        
        #thesetwo values work as follows
        #sizechange=round(uniform(-range,range)+positiveBias)
        #in english (+-range) +positive bias
        self.sizeChangeOrbRange=3
        self.sizeChangeOrbPositiveBias=2
        

        #how close can orbs be to getting eaten at spawn
        self.orbSpawnBuffer=10

        #should make this least common divisor 
        #of moveing orb spawn and static orb spawn
        self.orbFactoryCallPeriod=100

        self.movingOrbSpawnPeriod=200
        self.staticOrbSpawnPeriod=100

        self.frameRate=60

        self.segmentLength=20
        self.round=5

        self.sheildDuration=300
        self.sheildCoolDown=1000
        #monitor scaling stuff
        screenWidth=root.winfo_screenwidth()-100
        screenHeight=root.winfo_screenheight()-100
        screenSize=[screenWidth,screenHeight]
        self.screenSize=screenSize
        self.halfOrbHitbox,self.normalTurningRadius,self.menuTurningRadius,self.snakeSpeed,self.movingOrbThrust,self.textCharacterWidth=scaleToResolution(screenSize)
        self.transformationLengths=[10,15]
        #only thing ever changed in game
        self.quit=False
config=Config()
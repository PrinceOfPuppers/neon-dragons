import tkinter
root=tkinter.Tk()

def scaleToResolution(screenSize):
    devWidth=1500
    userWidth=screenSize[0]
    widthRatio=userWidth/devWidth

    #the constant number in each is the desired value when screen width is 1500
    segmentLength=int(round(20*widthRatio))

    normalTurningRadius=int(round(70*widthRatio))

    menuTurningRadius=int(round(100*widthRatio))

    halfOrbHitBox=int(round(15*widthRatio))
    snakeSpeed=3*widthRatio

    textCharacterWidth=int(round(50*widthRatio))

    return(segmentLength,halfOrbHitBox,normalTurningRadius,menuTurningRadius,snakeSpeed,textCharacterWidth)




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

        self.gameLength=18000
        self.frameRate=60


        self.debug=False
        self.round=5

        #monitor scaling stuff
        screenWidth=root.winfo_screenwidth()-100
        screenHeight=root.winfo_screenheight()-100
        screenSize=[screenWidth,screenHeight]
        #screenSize=[500,500]
        self.screenSize=screenSize
        self.segmentLength,self.halfOrbHitbox,self.normalTurningRadius,self.menuTurningRadius,self.snakeSpeed,self.textCharacterWidth=scaleToResolution(screenSize)

        #only thing ever changed in game
        self.quit=False
config=Config()
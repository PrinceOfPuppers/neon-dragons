class Config:

    def __init__(self):
        
        #thesetwo values work as follows
        #sizechange=round(uniform(-range,range)+positiveBias)
        #in english (+-range) +positive bias
        self.sizeChangeOrbRange=3
        self.sizeChangeOrbPositiveBias=2
        
        self.halfOrbHitbox=5

        #how close can orbs be to getting eaten at spawn
        self.orbSpawnBuffer=10

        #should make this least common divisor 
        #of moveing orb spawn and static orb spawn
        self.orbFactoryCallPeriod=100

        self.movingOrbSpawnPeriod=200
        self.staticOrbSpawnPeriod=100

        self.gameLength=18000
        self.frameRate=60
        self.screenSize=[1000,1000]

        self.debug=False

config=Config()
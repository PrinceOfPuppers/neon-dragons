class StalkerAssets:
    def __init__(self):
        self.head=[[-1, -5.5], [-2.2, -2.26], [-0.8, 1.14], [-1.6, -2.26], [-0.6, -3.26], [0, 0.0], [0.6, -3.26], [1.6, -2.26], [0.8, 1.14], [2.2, -2.26], [1, -5.5]]
        self.eye=[[0.0,-3.5],[1,-4.0],[0.0,-4.6],[-1,-4]]
        #iris is given centered at the origin, each point will have added to it the iris center plus an offset to have it pointed at other player
        self.iris=[[0.0, 0.4], [-0.2, 0], [0, -0.4], [0.2, 0]]

        #iris offset doesnt work properly due to the lack of filling around eye
        self.irisOffset=0.1
        self.irisCenter=[0,-4]
        #this is segmentLength times speed
        self.assumedSegmentLength=5.5
        self.assumedNeckRadius=1

    def scaleHead(self,player):
        segmentLength=player.speed*player.segmentLength
        
        scalingRatio=segmentLength/self.assumedSegmentLength
        scaledHead=[]
        for point in self.head:
            newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
            scaledHead.append(newPoint)

        scaledNeckRadius=self.assumedNeckRadius*scalingRatio
        return(scaledHead,scaledNeckRadius)
    
    def scaleEye(self,player):
        segmentLength=player.speed*player.segmentLength
        scalingRatio=segmentLength/self.assumedSegmentLength

        scaledEye=[]
        for point in self.eye:
            newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
            scaledEye.append(newPoint)
        
        scaledIris=[]
        for point in self.iris:
            newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
            scaledIris.append(newPoint)
        
        scaledIrisCenter=[self.irisCenter[0]*scalingRatio,self.irisCenter[1]*scalingRatio]

        scaledIrisOffset=self.irisOffset*scalingRatio
        return(scaledEye,scaledIris,scaledIrisCenter,scaledIrisOffset)
        

            


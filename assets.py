from config import config
class StalkerAssets:
    def __init__(self):
        self.head1=[[-1, -5.5],[-1.5,-2.0],[-0.8,1.14],[-0.4,-1.0],[0.0,0.0],[0.4,-1.0],[0.8,1.14],[1.5,-2.0],[1,-5.5]]
        self.eye1=[[0.0,-2.5],[-0.8,-2.0],[0,-1.5],[0.8,-2.0]]
        self.iris1=[[0.0,-2.5],[-0.3,-2.0],[0,-1.5],[0.3,-2.0]]
        self.pupil1=[]

        self.head2=[[-1, -5.5], [-2.2, -2.26], [-0.8, 1.14], [-1.6, -2.26], [-0.6, -3.26], [0, 0.0], [0.6, -3.26], [1.6, -2.26], [0.8, 1.14], [2.2, -2.26], [1, -5.5]]
        self.eye2=[[0.0,-3.5],[1,-4.0],[0.0,-4.6],[-1,-4]]
        self.iris2=[[0.0, -3.5], [-0.2, -4], [0, -4.6], [0.2, -4]]
        self.pupil2=[]


        self.head3=[[-1,-5.5],[-3,-1.5],[-0.8,1.14],[-2.3,-1.5],[-1.4,-2.8],[-0.8,-1.4],[-0.8,-2.8],[0,0],[0.8,-2.8],[0.8,-1.4], [1.4,-2.8],[2.3,-1.5],[0.8,1.14],[3,-1.5],[1,-5.5]]
        self.eye3=[[0.0,-4.4],[-1.2,-3.6],[0.0,-2.8],[1.2,-3.6]]
        self.iris3=[[0.0,-4.4],[0.4,-3.6],[0.0,-2.8],[-0.4,-3.6]]
        self.pupil3=[[0.0,-3],[0.0,-4]]

        #this is segmentLength times speed
        self.assumedSegmentLength=5.5
        self.assumedNeckRadius=1

        #lengths where the head and/or tail change type
        self.transformaitonLengths=[10,15]

    def scaleHead(self,player):
        
        segmentLength=player.speed*player.segmentLength
        scalingRatio=segmentLength/self.assumedSegmentLength

        if player.styleType==1:
            scaledHead=[]
            for point in self.head1:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledHead.append(newPoint)

            scaledNeckRadius=self.assumedNeckRadius*scalingRatio

        elif player.styleType==2:
            scaledHead=[]
            for point in self.head2:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledHead.append(newPoint)

            scaledNeckRadius=self.assumedNeckRadius*scalingRatio

        elif player.styleType==3:
            scaledHead=[]
            for point in self.head3:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledHead.append(newPoint)

            scaledNeckRadius=self.assumedNeckRadius*scalingRatio
    
        return(scaledHead,scaledNeckRadius)
    
    def scaleEye(self,player):
        segmentLength=player.speed*player.segmentLength
        scalingRatio=segmentLength/self.assumedSegmentLength

        if player.styleType==1:
            scaledEye=[]
            for point in self.eye1:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledEye.append(newPoint)

            scaledIris=[]
            for point in self.iris1:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledIris.append(newPoint)
            
            scaledPupil=[]
            for point in self.pupil1:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledPupil.append(newPoint)


        elif player.styleType==2:
            scaledEye=[]
            for point in self.eye2:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledEye.append(newPoint)

            scaledIris=[]
            for point in self.iris2:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledIris.append(newPoint)
            
            scaledPupil=[]
            for point in self.pupil2:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledPupil.append(newPoint)
        

        elif player.styleType==3:
            scaledEye=[]
            for point in self.eye3:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledEye.append(newPoint)

            scaledIris=[]
            for point in self.iris3:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledIris.append(newPoint)
            
            scaledPupil=[]
            for point in self.pupil3:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledPupil.append(newPoint)


        return(scaledEye,scaledIris,scaledPupil)

class OrbAssets:
    def __init__(self):
        self.StaticSizeChangeOrb=[[[0, 3], [1, 2]], [[0, 3], [1, 4]], [[1, 4], [1, 5]], [[1, 5], [2, 5]], [[2, 5], [3, 6]], [[3, 6], [4, 5]], [[4, 5], [5, 5]], [[5, 5], [5, 4]], [[5, 4], [6, 3]], [[6, 3], [5,2]], [[5, 2], [5, 1]], [[5, 1], [4, 1]], [[4, 1], [3, 0]], [[3, 0], [2, 1]], [[2, 1], [1, 1]], [[1, 1], [1, 2]], [[2, 3], [3, 4]], [[3, 4], [4, 3]], [[4, 3], [3, 2]], [[3, 2], [2, 3]]]
        self.assumedStaticSizeChangeOrbWidth=6
        self.assumedStaticSizeChangeOrbOrigin=[3,3]
        
        self.MovingSizeChangeOrb=[[[0, 3], [1, 2]], [[0, 3], [1, 4]], [[1, 4], [1, 5]], [[1, 5], [2, 5]], [[2, 5], [3, 6]], [[3, 6], [4, 5]], [[4, 5], [5, 5]], [[5, 5], [5, 4]], [[5, 4], [6, 3]], [[6, 3], [5,2]], [[5, 2], [5, 1]], [[5, 1], [4, 1]], [[4, 1], [3, 0]], [[3, 0], [2, 1]], [[2, 1], [1, 1]], [[1, 1], [1, 2]], [[2, 3], [3, 4]], [[3, 4], [4, 3]], [[4, 3], [3, 2]], [[3, 2], [2, 3]]]
        self.assumedMovingSizeChangeOrbWidth=6
        self.assumedMovingSizeChangeOrbOrigin=[3,3]

    def scaleAndTranslateStaticSizeChangeOrb(self,desiredWidth):
        StaticSizeChangeOrb=[]
        StaticSizeChangeOrbDetail=[]

        for line in self.StaticSizeChangeOrb:
            xComp1=round((line[0][0]-self.assumedStaticSizeChangeOrbOrigin[0])*desiredWidth/self.assumedStaticSizeChangeOrbWidth,config.round)
            yComp1=round((line[0][1]-self.assumedStaticSizeChangeOrbOrigin[1])*desiredWidth/self.assumedStaticSizeChangeOrbWidth,config.round)
            point1=(xComp1,yComp1)

            xComp2=round((line[1][0]-self.assumedStaticSizeChangeOrbOrigin[0])*desiredWidth/self.assumedStaticSizeChangeOrbWidth,config.round)
            yComp2=round((line[1][1]-self.assumedStaticSizeChangeOrbOrigin[1])*desiredWidth/self.assumedStaticSizeChangeOrbWidth,config.round)
            point2=(xComp2,yComp2)
            StaticSizeChangeOrb.append([point1,point2])
        

        return(StaticSizeChangeOrb)
    
    def scaleAndTranslateMovingSizeChangeOrb(self,desiredWidth):
        MovingSizeChangeOrb=[]
        MovingSizeChangeOrbDetail=[]
        
        for line in self.MovingSizeChangeOrb:
            xComp1=round((line[0][0]-self.assumedMovingSizeChangeOrbOrigin[0])*desiredWidth/self.assumedMovingSizeChangeOrbWidth,config.round)
            yComp1=round((line[0][1]-self.assumedMovingSizeChangeOrbOrigin[1])*desiredWidth/self.assumedMovingSizeChangeOrbWidth,config.round)
            point1=(xComp1,yComp1)

            xComp2=round((line[1][0]-self.assumedMovingSizeChangeOrbOrigin[0])*desiredWidth/self.assumedMovingSizeChangeOrbWidth,config.round)
            yComp2=round((line[1][1]-self.assumedMovingSizeChangeOrbOrigin[1])*desiredWidth/self.assumedMovingSizeChangeOrbWidth,config.round)
            point2=(xComp2,yComp2)

            MovingSizeChangeOrb.append([point1,point2])
        
        return(MovingSizeChangeOrb)

orbAssets=OrbAssets()
stalkerAssets=StalkerAssets()

            


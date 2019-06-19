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
        self.pupil3=[[0.0,-2.8],[0.0,-4.4]]

        #this is segmentLength times speed
        self.assumedSegmentLength=5.5
        self.assumedNeckRadius=1

        #lengths where the head and/or tail change type
        self.transformaitonLengths=[10,15]

    def scaleHead(self,player):
        #note this is always run first, so it sets the style type of the player, which in turn will be read by the
        #other scale methods
        #head types are 1 ,2 , ...
        styleType=1
        for i in range(0,len(self.transformaitonLengths)):
            transformationLength=self.transformaitonLengths[i]
            if player.length>=transformationLength:
                styleType+=1
            
            else:
                break
        print(styleType)
        segmentLength=player.speed*player.segmentLength
        scalingRatio=segmentLength/self.assumedSegmentLength

        if styleType==1:
            scaledHead=[]
            for point in self.head1:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledHead.append(newPoint)

            scaledNeckRadius=self.assumedNeckRadius*scalingRatio

        elif styleType==2:
            scaledHead=[]
            for point in self.head2:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledHead.append(newPoint)

            scaledNeckRadius=self.assumedNeckRadius*scalingRatio

        elif styleType==3:
            scaledHead=[]
            for point in self.head3:
                newPoint=[point[0]*scalingRatio,point[1]*scalingRatio]
                scaledHead.append(newPoint)

            scaledNeckRadius=self.assumedNeckRadius*scalingRatio
    
        return(scaledHead,scaledNeckRadius,styleType,self.transformaitonLengths)
    
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

    
        

            


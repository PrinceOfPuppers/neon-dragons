#print((5-7)%8)
#
#print(5%8 -6%8)
def modDistance(val1,val2,mod):
    modVal1=val1
    modVal2=val2

    diff1=abs((modVal1-modVal2)%mod)
    diff2=abs((modVal2-modVal1)%mod)
    
    if diff1<diff2:
        return(diff1)
    return(diff2)


for i in range(0,8):
    print(modDistance(i,i+5,8))
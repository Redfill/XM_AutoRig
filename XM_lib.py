import pymel.core as pm

def XMFixElbow(x, p1, p2, p3):
    armPos = p1.getTranslation("world")
    elbowPos = p2.getTranslation("world")
    handPos = p3.getTranslation("world")
    if(x == "x"):
        if(armPos[1] == handPos[1]):
            p2.setTranslation((elbowPos[0], handPos[2], elbowPos[2]), "world")
            pass
        a = (armPos[1]-handPos[1])/(armPos[0]-handPos[0])
        b = armPos[1]-(armPos[0]*a)
        c = (elbowPos[0]*a)+b
        p2.setTranslation((elbowPos[0], c, elbowPos[2]), "world")
    else:
        if(armPos[0] == handPos[0]):
            p2.setTranslation((handPos[0], elbowPos[1], elbowPos[2]), "world")
            pass
        a = (armPos[0] - handPos[0]) / (armPos[1] - handPos[1])
        b = armPos[0] - (armPos[1] * a)
        c = (elbowPos[1]*a)+b
        p2.setTranslation((c,elbowPos[1],elbowPos[2]), "world")
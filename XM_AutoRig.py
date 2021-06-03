import pymel.core as pm
from functools import partial

class locatorRig(object):
    def __init__(self, name, parent, location):
        self.name = name
        self.parent = parent
        self.location = location
        self.locator = pm.spaceLocator(n=self.name)

        self.locator.setTranslation(self.location, "world")

        if self.parent != None:
            self.locator.setParent(self.parent)



def CreateSetup(rigName):
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=True)

    rig_dict = {}
    hips = locatorRig("hips", None, (0,100,0))

    neck = locatorRig("neck", hips.locator, (0,155,0))

    head = locatorRig("head", neck.locator, (0,160,0))

    thigh = locatorRig("thigh", hips.locator, (12,95,0))

    leg = locatorRig("leg", thigh.locator, (12,49,0))

    foot = locatorRig("foot", leg.locator, (12,7,-3))

    shoulder = locatorRig("shoulder", neck.locator, (8,152,0))

    arm = locatorRig("arm", shoulder.locator, (18, 145,0))

    forearm = locatorRig("forearm", arm.locator, (30,120,1))

    hand = locatorRig("hand", arm.locator, (42,95,2))


    #save all locator to a dict for acces in other functions
    rig_dict["hips"] = hips.locator
    rig_dict["neck"] = neck.locator
    rig_dict["head"] = head.locator
    rig_dict["thigh"] = thigh.locator
    rig_dict["leg"] = leg.locator
    rig_dict["foot"] = foot.locator
    rig_dict["shoulder"] = shoulder.locator
    rig_dict["arm"] = arm.locator
    rig_dict["forearm"] = forearm.locator
    rig_dict["hand"] = hand.locator


    XMAutorigWindow.rigLocator = rig_dict
    print(XMAutorigWindow.rigLocator)

def DeleteSetup():
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=False)
    pm.delete(XMAutorigWindow.rigLocator["hips"])


def FixElbow():
    armPos = XMAutorigWindow.rigLocator["arm"].getTranslation("world")
    elbowPos = XMAutorigWindow.rigLocator["forearm"].getTranslation("world")
    handPos = XMAutorigWindow.rigLocator["hand"].getTranslation("world")
    a = (armPos[1]-handPos[1])/(armPos[0]-handPos[0])
    b = armPos[1]-(armPos[0]*a)
    c = (elbowPos[0]*a)+b
    XMAutorigWindow.rigLocator["forearm"].setTranslation((elbowPos[0],c,elbowPos[2]), "world")

class XMAutoRig(object):
    def __init__(self):

        self.window = "XMAutoRig"
        self.title = "XM Auto Rig"
        self.size = (500,200)

        # close old window is open
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)


        self.rigLocator = {}
        # create new window
        self.window = pm.window(self.window, title=self.title, widthHeight=self.size)
        currentRig = None
        pm.frameLayout(l="rig creator")
        pm.columnLayout()
        rigN = pm.textFieldGrp(l="rig name")
        pm.setParent(u=True)
        pm.rowLayout(nc=2, adj=True)
        pm.button(l="setup", c=lambda x: CreateSetup(rigN.getText()))
        pm.button(l="remove setup", c=lambda x: DeleteSetup())
        pm.setParent(u=True)
        self.settingFrame = pm.frameLayout(l="setting", en=False)
        pm.button(l="fix elbow", c=lambda x: FixElbow())
        pm.intSliderGrp(l="spine joint", v=3, min=0,max=6, f=True)



        # display new window
        pm.showWindow()

XMAutorigWindow = XMAutoRig()

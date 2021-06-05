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


class jointRig(object):
    def __init__(self, name, parent, location, type):
        self.name = name
        self.parent = parent
        self.location = location
        self.type = type
        if self.parent != None:
            self.joint = pm.joint(n=self.name,p=self.location)
            self.joint.setParent(self.parent)
            pm.joint(self.joint, e=True, sao="yup",zso=True, oj="xyz")
            self.joint.addAttr("XMjointType", dt="string")
            self.joint.setAttr("XMjointType", self.type)
        else:
            self.joint = pm.joint(n=self.name,p=self.location)
            pm.joint(self.joint, e=True, sao="yup", zso=True, oj="xyz")
            self.joint.addAttr("XMjointType", dt="string")
            self.joint.setAttr("XMjointType", self.type)

#setup locator setup
def CreateSetup(rigName):
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=True)

    rig_dict = {}
    hips = locatorRig("hips", None, (0,100,0))

    neck = locatorRig("neck", hips.locator, (0,155,0))

    head = locatorRig("head", neck.locator, (0,160,0))

    thigh = locatorRig("thigh", hips.locator, (12,95,0))

    leg = locatorRig("leg", thigh.locator, (12,49,0))

    foot = locatorRig("foot", thigh.locator, (12,7,-4))

    toe = locatorRig("toe", foot.locator, (12,1.5,11))

    toeEnd = locatorRig("toeEnd", toe.locator, (12,1.5,16))

    shoulder = locatorRig("shoulder", hips.locator, (8,152,0))

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
    rig_dict["toe"] = toe.locator
    rig_dict["toeEnd"] = toeEnd.locator
    rig_dict["shoulder"] = shoulder.locator
    rig_dict["arm"] = arm.locator
    rig_dict["forearm"] = forearm.locator
    rig_dict["hand"] = hand.locator


    XMAutorigWindow.rigLocator = rig_dict
    print(XMAutorigWindow.rigLocator)

#set up the base deformer joint
def Createjoint():
    locator = XMAutorigWindow.rigLocator
    rig_dict = {}
    pm.select(clear=True)
    #vertebre joints
    hips = jointRig("hips_bjnt", None, locator["hips"].getTranslation("world"), "spine")
    spine = jointRig("spine_bjnt", hips.joint, (locator["hips"].getTranslation("world") + locator["neck"].getTranslation("world"))/2,  "spine")
    neck = jointRig("neck_bjnt", spine.joint, locator["neck"].getTranslation("world"),  "spine")
    head = jointRig("head_bjnt", neck.joint, locator["head"].getTranslation("world"), "spine")

    #leg joints
    pm.select(clear=True)
    thigh = jointRig("l_upleg_bjnt", hips.joint, locator["thigh"].getTranslation("world"), "leg")
    leg = jointRig("l_leg_bjnt", thigh.joint, locator["leg"].getTranslation("world"), "leg")
    foot = jointRig("l_foot_bjnt", leg.joint, locator["foot"].getTranslation("world"), "leg")
    toe = jointRig("l_toe_bjnt", foot.joint, locator["toe"].getTranslation("world"), "leg")
    toeEnd = jointRig("l_toeEnd_jnt", toe.joint, locator["toeEnd"].getTranslation("world"), "leg")
    pm.joint(thigh.joint, e=True, oj="xyz", ch=True)

    #arm joints
    pm.select(clear=True)
    shoulder = jointRig("l_shoulder_bjnt", None, locator["shoulder"].getTranslation("world"), "shoulder")
    arm = jointRig("l_arm_bjnt", shoulder.joint, locator["arm"].getTranslation("world"), "arm")
    forearm = jointRig("l_forearm_bjnt", arm.joint, locator["forearm"].getTranslation("world"), "arm")
    hand = jointRig("l_hand_bjnt", forearm.joint, locator["hand"].getTranslation("world"), "arm")
    pm.joint(shoulder.joint, e=True, oj="xyz", ch=True )

    #save joint to dict
    rig_dict["hips"] = hips.joint
    rig_dict["spine"] = spine.joint
    rig_dict["neck"] = neck.joint
    rig_dict["head"] = head.joint
    rig_dict["thigh"] = thigh.joint
    rig_dict["leg"] = leg.joint
    rig_dict["foot"] = foot.joint
    rig_dict["toe"] = toe.joint
    rig_dict["toeEnd"] = toeEnd.joint
    rig_dict["shoulder"] = shoulder.joint
    rig_dict["arm"] = arm.joint
    rig_dict["forearm"] = forearm.joint
    rig_dict["hand"] = hand.joint

    XMAutorigWindow.rigJoint = rig_dict

def CreateCtrl():
    print("test")

def DeleteSetup():
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=False)
    pm.delete(XMAutorigWindow.rigLocator["hips"])


def FixElbow(x, p1, p2, p3):
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

class XMAutoRig(object):
    def __init__(self):

        self.window = "XMAutoRig"
        self.title = "XM Auto Rig"
        self.size = (500,400)

        # close old window is open
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)


        self.rigLocator = {}
        self.rigJoint= {}

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
        pm.rowLayout(nc=2)
        pm.button(l="fix elbow", c=lambda x: FixElbow("x",XMAutorigWindow.rigLocator["arm"], XMAutorigWindow.rigLocator["forearm"], XMAutorigWindow.rigLocator["hand"]))
        pm.button(l="fix knee",c=lambda x: FixElbow("y", XMAutorigWindow.rigLocator["thigh"], XMAutorigWindow.rigLocator["leg"],XMAutorigWindow.rigLocator["foot"]))
        pm.setParent(u=True)
        pm.intSliderGrp(l="spine joint", v=3, min=0,max=6, f=True)
        pm.frameLayout(l="create rig")
        pm.button(l="joint setup", c=lambda x: Createjoint())
        pm.button(l="ctrl setup", c=lambda x: CreateCtrl())



        # display new window
        pm.showWindow()

XMAutorigWindow = XMAutoRig()

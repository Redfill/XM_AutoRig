import pymel.core as pm
from string import replace
from functools import partial

class XMlocatorRig(object):
    def __init__(self, name, parent, location):
        self.name = name
        self.parent = parent
        self.location = location
        self.locator = pm.spaceLocator(n=self.name)

        self.locator.setTranslation(self.location, "world")

        if self.parent != None:
            self.locator.setParent(self.parent)


class XMjointRig(object):
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

class XMCircleRig(object):
    def __init__(self, joint, parent):
        self.joint = joint
        self.parent = parent
        self.circle = pm.circle(nr=(0,1,0), n=replace(self.joint.name(), "_bjnt", "_ctrl"), r=10)
        pm.matchTransform(self.circle, self.joint)
        pm.parentConstraint(self.circle,self.joint)
        if self.parent != None:
            pm.parent(self.circle,self.parent)


#setup locator setup
def XMCreateSetup(rigName):
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=True)

    rig_dict = {}
    hips = XMlocatorRig("hips", None, (0, 100, 0))

    neck = XMlocatorRig("neck", hips.locator, (0, 155, 0))

    head = XMlocatorRig("head", neck.locator, (0, 160, 0))

    thigh = XMlocatorRig("thigh", hips.locator, (12, 95, 0))

    leg = XMlocatorRig("leg", thigh.locator, (12, 49, 0))

    foot = XMlocatorRig("foot", thigh.locator, (12, 7, -4))

    toe = XMlocatorRig("toe", foot.locator, (12, 1.5, 11))

    toeEnd = XMlocatorRig("toeEnd", toe.locator, (12, 1.5, 16))

    shoulder = XMlocatorRig("shoulder", hips.locator, (8, 152, 0))

    arm = XMlocatorRig("arm", shoulder.locator, (18, 145, 0))

    forearm = XMlocatorRig("forearm", arm.locator, (30, 120, 1))

    hand = XMlocatorRig("hand", arm.locator, (42, 95, 2))


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

#set up the base deformer joint
def XMCreatejoint():
    locator = XMAutorigWindow.rigLocator
    rig_dict = {}
    pm.select(clear=True)
    #vertebre joints
    hips = XMjointRig("hips_bjnt", None, locator["hips"].getTranslation("world"), "spine")
    spines = XMSpineJoints(locator, hips)
    neck = XMjointRig("neck_bjnt", spines["spine" + str(XMAutorigWindow.Nspine.getValue() - 1)], locator["neck"].getTranslation("world"), "spine")
    head = XMjointRig("head_bjnt", neck.joint, locator["head"].getTranslation("world"), "spine")

    #leg joints
    pm.select(clear=True)
    thigh = XMjointRig("l_upleg_bjnt", hips.joint, locator["thigh"].getTranslation("world"), "leg")
    leg = XMjointRig("l_leg_bjnt", thigh.joint, locator["leg"].getTranslation("world"), "leg")
    foot = XMjointRig("l_foot_bjnt", leg.joint, locator["foot"].getTranslation("world"), "leg")
    toe = XMjointRig("l_toe_bjnt", foot.joint, locator["toe"].getTranslation("world"), "leg")
    toeEnd = XMjointRig("l_toeEnd_jnt", toe.joint, locator["toeEnd"].getTranslation("world"), "leg")
    pm.joint(thigh.joint, e=True, oj="xyz", ch=True)

    #arm joints
    pm.select(clear=True)
    shoulder = XMjointRig("l_shoulder_bjnt", spines["spine" + str(XMAutorigWindow.Nspine.getValue() - 1)], locator["shoulder"].getTranslation("world"), "shoulder")
    arm = XMjointRig("l_arm_bjnt", shoulder.joint, locator["arm"].getTranslation("world"), "arm")
    forearm = XMjointRig("l_forearm_bjnt", arm.joint, locator["forearm"].getTranslation("world"), "arm")
    hand = XMjointRig("l_hand_bjnt", forearm.joint, locator["hand"].getTranslation("world"), "arm")
    pm.joint(shoulder.joint, e=True, oj="xyz", ch=True )

    #save joint to dict
    rig_dict["hips"] = hips.joint
    rig_dict.update(spines)
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

def XMCreateCtrl():
    joints = XMAutorigWindow.rigJoint
    hc = joints["hips"].listRelatives(ad=True)
    hc.append(joints["hips"])
    hc.reverse()
    lastValid = joints["hips"]

    for joint in hc:
        if joint.getAttr("XMjointType") == "spine":
            print(lastValid)
            if lastValid != joints["hips"]:
                ctrl = XMCircleRig(joint, lastValid)
            else:
                ctrl = XMCircleRig(joint, None)

            lastValid = ctrl.circle
def XMDeleteSetup():
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=False)
    pm.delete(XMAutorigWindow.rigLocator["hips"])

def XMImportSetup():
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=True)
    rig_dict = {}
    select = pm.ls(sl=True,tr=True, dag=True)
    for s in select:
        rig_dict[s.name()] = s
    XMAutorigWindow.rigLocator = rig_dict

def XMImportJoint():
    rig_dict = {}
    select = pm.ls(sl=True,tr=True, dag=True)
    for s in select:
        rig_dict[s.name()] = s
    XMAutorigWindow.rigJoint = rig_dict

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

def XMSpineJoints(locator, hips):
    Nspine = XMAutorigWindow.Nspine.getValue()
    spines = {}
    dif = (locator["neck"].getTranslation("world") - locator["hips"].getTranslation("world"))/(Nspine+1)
    for i in range(Nspine):
        pos = locator["hips"].getTranslation("world") + (dif * (i+1))
        if i == 0:
            spine = XMjointRig("spine_bjnt", hips.joint, pos, "spine")
        else:
            spine = XMjointRig("spine" + str(i) + "_bjnt", spines["spine" + str(i - 1)], pos, "spine")
        spines["spine" + str(i)] = spine.joint
    return spines

def XMSetupUnparent():
    select = pm.ls(sl=True, tr=True)
    for s in select:
        s.setParent(XMAutorigWindow.rigLocator["hips"])

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
        pm.menuBarLayout()
        pm.menu(l="Import")
        pm.menuItem(l="Import setup", c=lambda x: XMImportSetup())
        pm.menuItem(l="Import joint", c=lambda x: XMImportJoint())

        currentRig = None
        pm.frameLayout(l="rig creator")
        pm.columnLayout()
        rigN = pm.textFieldGrp(l="rig name")
        pm.setParent(u=True)
        pm.rowLayout(nc=2, adj=True)
        pm.button(l="setup", c=lambda x: XMCreateSetup(rigN.getText()))
        pm.button(l="remove setup", c=lambda x: XMDeleteSetup())
        pm.setParent(u=True)
        self.settingFrame = pm.frameLayout(l="setting", en=False)
        #setup fixes
        pm.rowLayout(nc=3)
        pm.button(l="fix elbow", c=lambda x: XMFixElbow("x", XMAutorigWindow.rigLocator["arm"], XMAutorigWindow.rigLocator["forearm"], XMAutorigWindow.rigLocator["hand"]))
        pm.button(l="fix knee", c=lambda x: XMFixElbow("y", XMAutorigWindow.rigLocator["thigh"], XMAutorigWindow.rigLocator["leg"], XMAutorigWindow.rigLocator["foot"]))
        pm.button(l="unparent", c=lambda x: XMSetupUnparent())
        pm.setParent(u=True)
        self.Nspine = pm.intSliderGrp(l="spine joint", v=3, min=1,max=6, fmx=100, f=True)
        pm.frameLayout(l="create rig")
        pm.button(l="joint setup", c=lambda x: XMCreatejoint())
        pm.button(l="ctrl setup", c=lambda x: XMCreateCtrl())



        # display new window
        pm.showWindow()

XMAutorigWindow = XMAutoRig()

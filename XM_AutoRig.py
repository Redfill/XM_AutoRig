import pymel.core as pm
import sys
sys.path.append(pm.internalVar(usd=True) + "XM_AutoRig")
from XM_AutoRigFrame import XM_AutoRigFrame as rf
reload(rf)

#setup locator setup
def XMCreateSetup(rigName):
    pm.frameLayout(XMAutorigWindow.settingFrame, e=True, en=True)

    rig_dict = {}
    hips = rf.XMlocatorRig("hips", None, (0, 100, 0))

    neck = rf.XMlocatorRig("neck", hips.locator, (0, 155, 0))

    head = rf.XMlocatorRig("head", neck.locator, (0, 160, 0))

    thigh = rf.XMlocatorRig("thigh", hips.locator, (12, 95, 0))

    leg = rf.XMlocatorRig("leg", thigh.locator, (12, 49, 0))

    foot = rf.XMlocatorRig("foot", thigh.locator, (12, 7, -4))

    toe = rf.XMlocatorRig("toe", foot.locator, (12, 1.5, 11))

    toeEnd = rf.XMlocatorRig("toeEnd", toe.locator, (12, 1.5, 16))

    shoulder = rf.XMlocatorRig("shoulder", hips.locator, (8, 152, 0))

    arm = rf.XMlocatorRig("arm", shoulder.locator, (18, 145, 0))

    forearm = rf.XMlocatorRig("forearm", arm.locator, (30, 120, -2))

    hand = rf.XMlocatorRig("hand", arm.locator, (42, 95, 2))


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
    hips = rf.XMjointRig("hips_bjnt", None, locator["hips"].getTranslation("world"), "spine")
    spines = XMSpineJoints(locator, hips.joint, "hips", "neck", XMAutorigWindow.Nspine.getValue(), "spine")
    necks = XMSpineJoints(locator, spines["spine" + str(XMAutorigWindow.Nspine.getValue() - 1)], "neck", "head",
                          XMAutorigWindow.Nneck.getValue(), "neck", MSJ=True)
    head = rf.XMjointRig("head_bjnt", necks["neck" + str(XMAutorigWindow.Nneck.getValue() - 1)], locator["head"].getTranslation("world"), "neck")
    EndJoint(head.joint)

    #leg joints
    pm.select(clear=True)
    thigh = rf.XMjointRig("l_upleg_bjnt", hips.joint, locator["thigh"].getTranslation("world"), "leg")
    leg = rf.XMjointRig("l_leg_bjnt", thigh.joint, locator["leg"].getTranslation("world"), "leg")
    foot = rf.XMjointRig("l_foot_bjnt", leg.joint, locator["foot"].getTranslation("world"), "feet")
    toe = rf.XMjointRig("l_toe_bjnt", foot.joint, locator["toe"].getTranslation("world"), "toe")
    toeEnd = rf.XMjointRig("l_toeEnd_jnt", toe.joint, locator["toeEnd"].getTranslation("world"), "toeEnd")
    pm.joint(thigh.joint, e=True, oj="xyz", ch=True)
    EndJoint(toeEnd.joint)

    twist = rf.XMlocatorRig("l_twist",toeEnd.joint, toeEnd.joint.getTranslation("world")+(0,0,2), t="ctrl")
    bankOut = rf.XMlocatorRig("l_bankOut",twist.locator, toeEnd.joint.getTranslation("world")+(5,0,-5), t="ctrl")
    bankIn = rf.XMlocatorRig("l_bankIn",bankOut.locator, toeEnd.joint.getTranslation("world")+(-5,0,-5), t="ctrl")
    heel = rf.XMlocatorRig("l_heel",bankIn.locator, toeEnd.joint.getTranslation("world")+(0,0,-20), t="ctrl")

    print("test")
    #arm joints
    pm.select(clear=True)
    shoulder = rf.XMjointRig("l_shoulder_bjnt", spines["spine" + str(XMAutorigWindow.Nspine.getValue() - 1)], locator["shoulder"].getTranslation("world"), "shoulder")
    arm = rf.XMjointRig("l_arm_bjnt", shoulder.joint, locator["arm"].getTranslation("world"), "arm")
    forearm = rf.XMjointRig("l_forearm_bjnt", arm.joint, locator["forearm"].getTranslation("world"), "forearm")
    hand = rf.XMjointRig("l_hand_bjnt", forearm.joint, locator["hand"].getTranslation("world"), "hand")
    pm.joint(shoulder.joint, e=True, oj="xyz", ch=True )
    EndJoint(hand.joint)

    #save joint to dict
    rig_dict["hips"] = hips.joint
    rig_dict.update(spines)
    rig_dict.update(necks)
    rig_dict["head"] = head.joint
    rig_dict["thigh"] = thigh.joint
    rig_dict["leg"] = leg.joint
    rig_dict["foot"] = foot.joint
    rig_dict["toe"] = toe.joint
    rig_dict["toeEnd"] = toeEnd.joint
    rig_dict["twist"] = twist.locator
    rig_dict["shoulder"] = shoulder.joint
    rig_dict["arm"] = arm.joint
    rig_dict["forearm"] = forearm.joint
    rig_dict["hand"] = hand.joint

    XMAutorigWindow.rigJoint = rig_dict

def XMCreateCtrl():
    joints = XMAutorigWindow.rigJoint

    Mastercurve = pm.circle(n="master_ctrl", nr=(0,1,0), r=40)
    MasterGroup = pm.group(Mastercurve, n=XMAutorigWindow.rigN.getText())

    #spine controller
    hc = joints["hips"].listRelatives(ad=True)
    hc.append(joints["hips"])
    hc.reverse()
    lastValid = joints["hips"]
    lastSpine = joints["hips"]
    for joint in hc:
        if joint.getAttr("XMjointType") == "spine" or joint.getAttr("XMjointType") == "neck":

            if lastValid != joints["hips"]:
                ctrl = rf.XMCurveRig(joint, lastValid, "circle", "", s=1.5, LT=True)
            else:
                ctrl = rf.XMCurveRig(joint, None, "circle", "", s=2)
                ctrl.group.setParent(Mastercurve)

            lastValid = ctrl.curve
            if joint.getAttr("XMjointType") == "spine":
                lastSpine = ctrl.curve

    #arm setup
    Rshoulder = pm.mirrorJoint(joints["shoulder"], mirrorYZ=True, mirrorBehavior=True, searchReplace=('l_', 'r_'))
    armCtrlSetup(Mastercurve,"l_", lastSpine, joints["shoulder"], joints["arm"], joints["forearm"], joints["hand"])

    armCtrlSetup(Mastercurve,"r_", lastSpine, pm.ls(Rshoulder[0])[0], pm.ls(Rshoulder[1])[0], pm.ls(Rshoulder[2])[0], pm.ls(Rshoulder[3])[0], m=True)

    #leg setup
    Rleg = pm.mirrorJoint(joints["thigh"], mirrorYZ=True, mirrorBehavior=True, searchReplace=("l_", "r_"))

    LegCtrlSetup(Mastercurve,"l_", joints["thigh"], joints["leg"], joints["foot"], joints["toe"], joints["toeEnd"])

    LegCtrlSetup(Mastercurve,"r_",pm.ls(Rleg[0])[0], pm.ls(Rleg[1])[0], pm.ls(Rleg[2])[0], pm.ls(Rleg[3])[0], pm.ls(Rleg[4])[0], m=True)

    jointGrp = pm.group(joints["hips"], n="joints")

    jointGrp.setParent(MasterGroup)

def armCtrlSetup(master,num, lastSpine ,shoulder, arm, forearm, hand, m=False):
    # arm FK controller
    shoulderCtrl = rf.XMCurveRig(shoulder, lastSpine, ctrl="Circle Pin", m=m)
    print("post")
    fkarm = pm.duplicate(arm, rc=True)
    fkcopies = fkarm[0].listRelatives(ad=True)
    fkcopies.append(fkarm[0])
    fkcopies.reverse()
    lastvalid = shoulderCtrl.curve
    armctrls = {}

    for joint in fkcopies:
        joint.rename(num + joint.getAttr("XMjointType") + "FK_jnt")
        ctrl = rf.XMCurveRig(joint, lastvalid, "circle", "fk", m=m, LT=True)
        armctrls[num + joint.getAttr("XMjointType") + "_fk"] = ctrl.curve
        lastvalid = armctrls[num + joint.getAttr("XMjointType") + "_fk"]

    #IK arm setup
    ikarm = pm.duplicate(arm, rc=True)
    ikcopies = ikarm[0].listRelatives(ad=True)
    ikcopies.append(ikarm[0])
    ikcopies.reverse()
    for joint in ikcopies:
        joint.rename(num + joint.getAttr("XMjointType") + "IK_jnt")

    ikHandle = pm.ikHandle(sj=ikcopies[0], ee=ikcopies[2], sol="ikRPsolver", n= num + "arm_ikHandle")
    ikCtrl = rf.XMCurveRig(ikHandle[0], None, "Sphere", "IK", "par", s=2, m=m)
    ikCtrl.group.setRotation(hand.getRotation("world"))
    pm.orientConstraint(ikCtrl.curve, ikcopies[2])

    ikPole = rf.XMCurveRig(ikcopies[1], ikCtrl.curve, "Sphere", "", "", m=m)
    ikPole.curve.setTranslation(ikPole.curve.getTranslation("world") + (0, 0, -70), "world")

    pm.poleVectorConstraint(ikPole.curve, ikHandle[0])

    ikOption = rf.XMCurveRig(hand, hand, "Gear", "ikOption", "ctrl", m=m)

    ikOption.curve.addAttr("IKFK", at="bool", k=True, r=True)


    armCont = pm.parentConstraint(fkcopies[0], ikcopies[0], arm)
    forearmCont = pm.parentConstraint(fkcopies[1], ikcopies[1], forearm)
    handCont = pm.parentConstraint(fkcopies[2], ikcopies[2], hand)

    reverseNode = pm.shadingNode("reverse", au=True)

    pm.connectAttr(ikOption.curve.IKFK, reverseNode.input.inputX)

    #arm
    pm.connectAttr(reverseNode.output.outputX, pm.parentConstraint(armCont, q=True, wal=True)[1])
    pm.connectAttr(ikOption.curve.IKFK, pm.parentConstraint(armCont, q=True, wal=True)[0])

    #forearm
    pm.connectAttr(reverseNode.output.outputX, pm.parentConstraint(forearmCont, q=True, wal=True)[1])
    pm.connectAttr(ikOption.curve.IKFK, pm.parentConstraint(forearmCont, q=True, wal=True)[0])

    #hand
    pm.connectAttr(reverseNode.output.outputX, pm.parentConstraint(handCont, q=True, wal=True)[1])
    pm.connectAttr(ikOption.curve.IKFK, pm.parentConstraint(handCont, q=True, wal=True)[0])

    for joint in armctrls:
        pm.connectAttr(ikOption.curve.IKFK, armctrls[joint].visibility)
    pm.connectAttr(reverseNode.output.outputX, ikCtrl.curve.visibility)
    ikarm[0].hide()
    fkarm[0].hide()
    ikHandle[0].hide()

    ikCtrl.group.setParent(master)

def LegCtrlSetup(master,num, thigh, leg, foot, toe, toeEnd, m=False):
    twist = toeEnd.listRelatives(ad=True, typ="transform")
    twist.reverse()

    legIkHandle = pm.ikHandle(sj=thigh, ee=foot, sol="ikRPsolver", n=num + "leg_ikHandle")
    ikCtrl = rf.XMCurveRig(legIkHandle[0], None, "Sphere", "IK", "par", s=2, m=m)

    twist[0].setParent(ikCtrl.curve)

    ikPole = rf.XMCurveRig(leg, ikCtrl.curve, "Sphere", "", "", m=m)
    ikPole.curve.setTranslation(ikPole.curve.getTranslation("world") + (0, 0, 70), "world")

    pm.poleVectorConstraint(ikPole.curve, legIkHandle[0])
    toeIkhanlde = pm.ikHandle(sj=foot, ee=toe, sol="ikSCsolver", n=num + "toe_ikHandle")
    toeEndIkhandle = pm.ikHandle(sj=toe, ee=toeEnd, sol="ikSCsolver", n=num + "toeEnd_ikHandle")

    heelCtrl = rf.XMCurveRig(twist[3], twist[2], "Half Sphere", "", par=None, m=m)

    toeRollCtrl = rf.XMCurveRig(twist[0], heelCtrl.curve, "Half Sphere", "", par=None, m=m)

    footRollCtrl = rf.XMCurveRig(toeIkhanlde[0], toeRollCtrl.curve, "circle", "", par=None, s=0.8, m=m)

    toeFlapCtrl = rf.XMCurveRig(toeIkhanlde[0], toeRollCtrl.curve, "circle", "", par=None, s=0.4, m=m)

    legIkHandle[0].setParent(footRollCtrl.curve)
    toeIkhanlde[0].setParent(footRollCtrl.curve)
    toeEndIkhandle[0].setParent(toeFlapCtrl.curve)

    ikCtrl.curve.addAttr("twist", at="float", k=True, r=True)
    ikCtrl.curve.addAttr("bankOut", at="float", k=True, r=True)
    ikCtrl.curve.addAttr("bankIn", at="float", k=True, r=True)

    pm.connectAttr(ikCtrl.curve.twist, twist[0].rotateY)
    pm.connectAttr(ikCtrl.curve.bankOut, twist[1].rotateZ)
    pm.connectAttr(ikCtrl.curve.bankIn, twist[2].rotateZ)

    legIkHandle[0].hide()
    toeIkhanlde[0].hide()
    toeEndIkhandle[0].hide()

    ikCtrl.group.setParent(master)

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
    "not really functional now that the joint and ctrl setup as gotten more complex"
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


def XMSpineJoints(locator, startJ, startL, endL, value, Num, MSJ=False):
    """
    create x number of joint between two locator
    :param locator: dict of locators
    :param startJ: parent of the chain
    :param startL: starting locator
    :param endL: end locator
    :param value: number of joints
    :param Num: type of the joint
    :param MSJ: Make Starting Joint: whether or not the create the initial joint of the chain
    :return: return an dict of the created joints
    """
    if MSJ == False:
        offset=1
    else:
        offset=0
    spines = {}
    dif = (locator[endL].getTranslation("world") - locator[startL].getTranslation("world"))/(value+offset)
    for i in range(value):
        pos = locator[startL].getTranslation("world") + (dif * (i+offset))
        if i == 0:
            spine = rf.XMjointRig(Num+"_bjnt", startJ, pos, Num)
        else:
            spine = rf.XMjointRig(Num + str(i) + "_bjnt", spines[Num + str(i - 1)], pos, Num)
        spines[Num + str(i)] = spine.joint
    return spines

def XMSetupUnparent():
    select = pm.ls(sl=True, tr=True)
    for s in select:
        s.setParent(XMAutorigWindow.rigLocator["hips"])

def EndJoint(joint):
    joint.setAttr("jointOrientX", 0)
    joint.setAttr("jointOrientY", 0)
    joint.setAttr("jointOrientZ", 0)

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
        pm.menuItem(l="Import setup", c=lambda x1: XMImportSetup())
        pm.menuItem(l="Import joint", c=lambda x: XMImportJoint())

        currentRig = None
        pm.frameLayout(l="rig creator")
        pm.columnLayout()
        self.rigN = pm.textFieldGrp(l="rig name")
        pm.setParent(u=True)
        pm.rowLayout(nc=2, adj=True)
        pm.button(l="setup", c=lambda x: XMCreateSetup(self.rigN.getText()))
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
        self.Nneck = pm.intSliderGrp(l="neck joint", v=2, min=1,max=6, fmx=100, f=True)
        pm.frameLayout(l="create rig")
        pm.button(l="joint setup", c=lambda x: XMCreatejoint())
        pm.button(l="ctrl setup", c=lambda x: XMCreateCtrl())



        # display new window
        pm.showWindow()

XMAutorigWindow = XMAutoRig()

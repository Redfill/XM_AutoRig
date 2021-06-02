import pymel.core as pm
from functools import partial
def CreateSetup(rigName):
    rig_dict = {}
    hips = pm.spaceLocator(n="hips")
    hips.setTranslation((0,100,0), "world")

    neck = pm.spaceLocator(n="neck")
    neck.setTranslation((0, 155, 0), "world")

    head = pm.spaceLocator(n="head")
    head.setTranslation((0, 162, 0), "world")

    print(hips)

    #save all locator to a dict for acces in other functions
    rig_dict["hips"] = hips
    rig_dict["neck"] = neck
    rig_dict["head"] = head


    XMAutorigWindow.rigLocator = rig_dict
    print(XMAutorigWindow.rigLocator)

def DeleteSetup():
    for i in XMAutorigWindow.rigLocator.values():
        pm.delete(i)
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
        pm.intSliderGrp(l="spine joint", v=3, min=0,max=6, f=True)


        # display new window
        pm.showWindow()

XMAutorigWindow = XMAutoRig()

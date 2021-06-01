import pymel.core as pm
from functools import partial

class rig:
    def __init__(self, rigName, *args):
        self.rigName = rigName

        self.hips = pm.spaceLocator(n="cog" + self.rigName)


    def moverig(self):
        self.hips.setLocation(1.0,2.0,3.0)

class XMAutoRig(object):
    def __init__(self):

        self.window = "XMAutoRig"
        self.title = "XM Auto Rig"
        self.size = (500,700)

        # close old window is open
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)

        # create new window
        self.window = pm.window(self.window, title=self.title, widthHeight=self.size)

        pm.frameLayout(l="rig creator")
        rigN = pm.textFieldGrp(l="rig name")
        pm.button(l="create rig", c=partial(rig, "a3dsi"))


        # display new window
        pm.showWindow()

XMWindow = XMAutoRig()

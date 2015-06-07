from Tkinter import *
import ttk
import random

class Die():
    """docstring for Die"""

    def __init__(self, parent, sType):
        self.station = sType
        self.faces = self.getFaces(sType)
        self.faceUpSide = random.choice(self.faces)
        self.imgNames = self.getImgNames(sType)
        self.isLocked = False
        self.widget = Label(parent, image = self.imgNames[self.faceUpSide])
        self.widget.pack(side = RIGHT)
        self.widget.bind("<Button-1>", self.toggleLock)


    def toggleLock(self, event):
        self.isLocked = not self.isLocked
        print "Locked", self.isLocked

    def getFaces(self, station):
        return range(1,7)

    def getImgNames(self, station):
        images = ["one.gif","two.gif","three.gif","four.gif","five.gif","six.gif"]
        return {x:images[x-1] for x in self.faces}



class DicePanel:
    """docstring for DicePanel"""
    def __init__(self, parent, sType):
        self.sType = sType
        self.frame = Frame(parent)
        self.frame.pack()
        self.diceCount = self.getCount(sType)
        self.dice = self.makeDice()

    def getCount(self, sType):
        return 4

    def makeDice(self):
        return [Die(self.frame, self.sType) for x in range(self.diceCount)]


if __name__ == "__main__":
    root = Tk()
    panel = DicePanel(root, "Engineering")
    root.mainloop()
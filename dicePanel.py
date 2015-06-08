from Tkinter import *
import ttk
import random

class Die():
    """docstring for Die"""

    def __init__(self, parent, sType):
        self.station = sType
        self.faces = self.getFaces(sType)
        self.faceUpSide = random.choice(self.faces)
        self.imgs = self.getImgs(sType)
        self.isLocked = False
        self.widget = Label(parent, image = self.imgs[self.faceUpSide])
        self.widget.pack(side = RIGHT)
        self.widget.bind("<Button-1>", self.toggleLock)


    def toggleLock(self, event):
        self.isLocked = not self.isLocked

    def getFaces(self, sType):
        return range(1,7)

    def getImgs(self, sType):
        imageNames = ["one.gif","two.gif","three.gif","four.gif","five.gif","six.gif"]
        images = [PhotoImage(file = name) for name in imageNames] 
        return {x:images[x-1] for x in self.faces}

    def reroll(self):
        self.faceUpSide = random.choice(self.faces)
        self.widget.configure(image = self.imgs[self.faceUpSide])




class DicePanel:
    """docstring for DicePanel"""
    def __init__(self, parent, sType):
        self.sType = sType
        self.frame = Frame(parent)
        self.frame.pack()
        self.diceCount = self.getCount(sType)
        self.dice = self.makeDice()
        self.rollButton = Button(self.frame, text="Reroll", command=self.rollDice)
        self.rollButton.pack(side = RIGHT)

    def getCount(self, sType):
        return 4

    def makeDice(self):
        return [Die(self.frame, self.sType) for x in range(self.diceCount)]

    def rollDice(self):
        for die in self.dice:
            if not die.isLocked:
                die.reroll()

if __name__ == "__main__":
    root = Tk()
    panel = DicePanel(root, "Engineering")
    root.mainloop()
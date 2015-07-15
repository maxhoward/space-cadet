from Tkinter import *
import ttk
import random

#added dieDict outside Die definition to:
#1. allow dice to learn their type via sType, obviating need for mostly redundant Die subclasses
#1a. while preventing newly created Die objects from making extra pointers to ultimately unnecessary lists/dicts
#2. provide a centralized location for all dice-related images, making them easily findable/editable

#lists of image names go here
wpList=['head.gif','body.gif','tail.gif','2hit.gif','1hit.gif','1hit.gif']
snList=[]
trList=[]
shList=[]
hmList=[]
egList=['one.gif','two.gif','three.gif','four.gif','five.gif''six.gif']


dieDict={
    "Weapons":wpList,
    "Sensors":snList,
    "Tractors":trList,
    "Shields":shList,
    "Helm":hmList,
    "Engineering":egList
}


class Die(object): 
    """docstring for Die"""

    def __init__(self, parent, panel):
        self.station = panel.sType
        self.faces = self.getFaces()
        self.faceUpSide = random.choice(self.faces)
        self.imgs = self.getImgs()
        self.isLocked = False
        self.widget = Label(parent, image = self.imgs[self.faceUpSide])
        self.widget.pack(side = LEFT)
        self.widget.bind("<Button-1>", self.toggleLock)
        self.panel = panel #reference to superclass. we could also do this with super(Die,self)
        global dieDict
        self.imageNames = dieDict[self.station]
        self.images = [PhotoImage(file = name) for name in self.imageNames] 


    def toggleLock(self, event):
        self.isLocked = not self.isLocked

    def getFaces(self):
        return range(1,7)

    def getImgs(self):
        return {x:self.images[x-1] for x in self.faces}

    def reroll(self):
        self.faceUpSide = random.choice(self.faces)
        self.widget.configure(image = self.imgs[self.faceUpSide])




class DicePanel(object):
    """docstring for DicePanel"""
    def __init__(self, parent):
        self.sType = "None"
        self.frame = Frame(parent)
        self.frame.pack()

        self.diceCount=4
        self.dice = self.makeDice()

        self.rollButton = Button(self.frame, text="Reroll", command=self.rollDice)
        self.rollButton.pack()
        self.rollButton = Button(self.frame, text="Print Locked Dice", command=self.getLockedDice)
        self.rollButton.pack()

    def makeDice(self):
        return [Die(parent=self.frame, panel=self) for x in range(self.diceCount)]

    def rollDice(self):
        for die in self.dice:
            if not die.isLocked:
                die.reroll()

    def getLockedDice(self):
        print [die.faceUpSide for die in self.dice if die.isLocked]

class WpPanel(DicePanel):

    def __init__(self,parent):
        super(WpPanel,self).__init__(parent)
        self.sType="Weapons"
        self.diceCount=6

    #1: head
    #2: body
    #3: tail
    #4: two hit
    #5||6: one hit

class SnPanel(DicePanel):

    def __init__(self,parent):
        DicePanel.__init__(self,parent,sType="Sensors")
        self.diceCount=4

    #1: one lock
    #2: two lock
    #3: one jam
    #4: two jam
    #5||6: star

class TrPanel(DicePanel):
        
    def __init__(self,parent):
        DicePanel.__init__(self,parent,sType="Tractors")
        self.diceCount=3

    #1: A mine
    #2: B mine
    #3: one pull
    #4: two pull
    #5||6: triangles!

class ShPanel(DicePanel):
    def __init__(self,parent):
        DicePanel.__init__(self,parent,sType="Shields")
        self.diceCount=3

    #note that FRBL order matches Ship.shields' ordering in space_cadets_board.py
    #1: front
    #2: right
    #3: back
    #4: left
    #5||6: weird circle things

    #logic for Ship grabbing Shields' info (will eventually be not here; key thing is that Ships are responsible for interpreting the panel's locked dice as shields)
    #this is OK because the only time shields need to be interpreted as such is when you're under attack, which means commands are going through Board() anyway
    #separately, the Shields Station will interpret the locked dice client-side in order to show the player their shield status
        #for x in ShPanelInstance.getLockedDice:
            #if x == 1: Ship.shields[F]++ #etc for 2, 3, 4; pass on 5/6


class HmPanel(DicePanel):
    def __init__(self,parent):
        DicePanel.__init__(self,parent,sType="Helm")
        self.diceCount=3

    #1: forward left
    #2: forward right
    #3: forward two
    #4: U-turn
    #5||6: forward one

class EgPanel(DicePanel):
    def __init__(self,parent):
        DicePanel.__init__(self,parent,sType="Engineering") 
        self.diceCount=6

    #faces operate normally for now; will interact with Station.py stations eventually

if __name__ == "__main__":
    root = Tk()
    panel = DicePanel(root, "Engineering")
    root.mainloop()
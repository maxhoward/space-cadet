from dicePanel import *

class WpPanel(DicePanel):

	def __init__(self,parent):
		DicePanel.__init__(self,parent,sType="Weapons")
		self.diceCount=6

	def makeDice(self,parent):
		return [WeaponsDie(self.frame, self.sType, self) for x in range(self.diceCount)]

class SnPanel(DicePanel):

	def __init__(self,parent):
		DicePanel.__init__(self,parent,sType="Sensors")
		self.diceCount=4

	def makeDice(self,parent):
		return [SensorsDie(self.frame, self.sType, self) for x in range(self.diceCount)]

class TrPanel(DicePanel):
		
	def __init__(self,parent):
		DicePanel.__init__(self,parent,sType="Tractors")
		self.diceCount=3
	def makeDice(self):
		return [TractorsDie(self.frame, self.sType, self) for x in range(self.diceCount)]

class ShPanel(DicePanel):
	def __init__(self,parent):
		DicePanel.__init__(self,parent,sType="Shields")
		self.diceCount=3

	def makeDice(self):
		return [ShieldsDie(self.frame, self.sType, self) for x in range(self.diceCount)]

class HmPanel(DicePanel):
	def __init__(self,parent):
		DicePanel.__init__(self,parent,sType="Helm")
		self.diceCount=3

	def makeDice(self):
		return [HelmDie(self.frame, self.sType, self) for x in range(self.diceCount)]

class EgPanel(DicePanel):
	def __init__(self,parent):
		DicePanel.__init__(self,parent,sType="Engineering")	
		self.diceCount=6
	def makeDice(self):
		return [EngDie(self.frame, self.sType, self) for x in range(self.diceCount)]

class WeaponsDie(Die):
	def __init__(self,parent,sType,panel):
		Die.__init__(self,parent,sType,panel)
		self.imageNames=[]
		self.images=[]

class SensorsDie(Die):
	def __init__(self,parent,sType,panel):
		Die.__init__(self,parent,sType,panel)
			self.imageNames=[]
			self.images=[]

class TractorsDie(Die):
	def __init__(self,parent,sType,panel):
		Die.__init__(self,parent,sType,panel)
			self.imageNames=[]
			self.images=[]


class ShieldsDie(Die):
	def __init__(self,parent,sType,panel):
		Die.__init__(self,parent,sType,panel)
			self.imageNames=[]
			self.images=[]

class HelmDie(Die):
	def __init__(self,parent,sType,panel):
		Die.__init__(self,parent,sType,panel)
			self.imageNames=[]
			self.images=[]


class EngDie(Die):
	def __init__(self,parent,sType,panel):
		Die.__init__(self,parent,sType,panel)
			self.imageNames=[]
			self.images=[]



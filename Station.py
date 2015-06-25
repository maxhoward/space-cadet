import Tkinter as tk
import ttk

"""
Station class: 
Handles user interactions with stations.
Each station includes a station bar widget, which can be clicked to enter or leave the station, and images to show locked dice.
Interactions: 
	Station->DicePanel (determines which station's DicePanel to show)
	DicePanel->Station (determines which stations are locked (Engineering DicePanel) and which dice are locked to a station (all others))

Terminology:
	Locked: An Engineering die is locked to this station and it can be entered
	Active: Player is currently rolling dice for this station
	Enter: Make a locked station active
	Leave: Roll dice for another station, but keep this station locked for future entry
	Free: Release this station's Engineering die, unlocking it

To test: run Station_test.py 
"""

class Station():


	def __init__(self,parent,name,superclass):
		self.name = name
		self.fr=tk.Frame(parent,bd=2, relief=tk.RAISED,width=200) #each station bar lives inside its own frame (for dice image packing)
		self.fr.pack()
		self.bar = tk.Label(self.fr, bg='LightSteelBlue1',text=self.name,width=20)
		self.bar.bind("<Button-1>",self.enter) #note: in order to use the bind notation, the bound function must have an additional argument to hold the event
		self.bar.bind("<Double-Button-1>",self.free)
		self.bar.pack(side=tk.LEFT)
		self.isActive = False #active status of the station (whether you're in it)
		self.isLocked = False #whether station has Eng dice locked in
		self.statDice = [] #list of locked station dice
		self.view = [self.isActive,self.isLocked,self.statDice] #necessary information to graphically represent the station bar on other player's console
		self.superclass = superclass
	
	def displayDice(self,newDice):
		self.statDice+=newDice
		for x in self.statDice:
			d=tk.Label(self.fr,text=x);
			d.pack(side=tk.LEFT);
		
	def hilite(self): #highlight the active station you are in 
	#triggered by enter(), free(), leave()
		if self.isActive:
			self.bar.configure(bg = 'lawn green');
		elif not self.isActive:
			self.bar.configure(bg = 'LightSteelBlue1');
		else: pass;
	
	def lock(self): #lock an Eng die to the station so other players can't click it
	#triggered on Eng die click
		self.isLocked = True;
	
	def enter(self,event): #enter the station, rendering it active
	#triggered by station label single click
		for x in self.superclass.stationList: x.leave(event)
		if self.isLocked and not self.isActive:
			self.isActive = True
			self.hilite()
		else:
			pass
	
	def free(self, event): #leave the station, freeing its die for Eng
	#note: you can click on another station to make it active (triggering leave()) without using free(). free() is only for when you want to free the die.
	#triggered by station label double-click
		if self.isLocked & self.isActive:
			self.isActive=False
			self.hilite()
			self.isLocked = False
		else: pass;
	
	def leave(self,event): #deactivate station so its dice no longer show in the action panel, without unlocking it
	#triggered by clicking on another station label
		self.isActive = False
		self.hilite()

	def getView(self):
		return self.view;

	





import Tkinter as tk
import ttk

class Station():

	
	def __init__(self,parent,name):
		self.name = name;
		self.fr=tk.Frame(parent,bd=2, relief=tk.RAISED,width=200);
		self.fr.pack();
		self.bar = tk.Button(self.fr, command=self.enter,bg='LightSteelBlue1',text=self.name,width=20);
		self.bar.pack(side=tk.LEFT);
		self.isActive = False; #active status of the station (whether you're in it)
		self.isLocked = False; #whether station has Eng dice locked in
		self.statDice = []; #list of locked station dice
		self.view = [self.isActive,self.isLocked,self.statDice];
	
	def displayDice(self):
		for x in self.statDice:
			k=str(x);
			d=tk.Label(self.fr,text=k);
			d.pack(side=tk.LEFT);
		
	def hilite(self): #highlight the active station you are in 
	#triggered by enter(), free(), leave()
		if self.isActive:
			self.bar.configure(bg = 'LightSteelBlue1');
		elif not self.isActive:
			self.bar.configure(bg = 'lawn green');
		else: pass;
	
	def lock(self): #lock a die to the station so other players can't click it
	#triggered on Eng die click
		self.isLocked = True;
	
	def enter(self): #enter the station, rendering it active
	#triggered by station label single click
		if self.isLocked:
			self.hilite();
			self.isActive = True;
		else:
			pass;
	
	def free(self): #leave the station, freeing its die for Eng
	#note: you can click on another station to make it active (triggering leave()) without using free(). free() is only for when you want to free the die.
	#triggered by station label double-click
		self.hilite();
		self.isActive = False;
		self.isLocked = False;
	
	def leave(self): #deactivate station so its dice no longer show in the action panel, without unlocking it
	#triggered by clicking on another station label
		self.hilite();
		self.isActive = False;
	
	def getView(self):
		return self.view;
		
#import the above and then run the following script to test:
#root=tk.Tk();
#helm = Station(root,"Helm");
#helm.lock();
#root.mainloop();

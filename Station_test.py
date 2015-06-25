import Tkinter as tk
from Station import *



class Station_test():
	def __init__(self):

		self.activeStations=[]
		self.stationList=[]

		self.stationNames=[
			"Weapons",
			"Sensors",
			"Tractors",
			"Shields",
			"Helm",
			"Engineering"
		]

		for x in self.stationNames:
			self.stationList.append(Station(root,x,self))
		for y in self.stationList: y.lock()

	

root=tk.Tk()
Station_test()
root.mainloop()




from tkinter import *
import ttk
import random

class Die():
 	"""docstring for Die"""

 	def __init__(self, parent, type, pos):
 		self.station = station
 		self.faces = getFaces(station)
 		self.imgNames = getImgNames(station)
 		self.isLocked = False
 		self.widget = Label(parent, img = self.imgNames[0])
 		self.widget.pack(side = RIGHT)

 	def getFaces(station):
 		return range(1,7)

 	def getImgNames(station):
 		return ["one.gif","two.gif","three.gif","four.gif","five.gif","six.gif"]





class DicePanel:
	"""docstring for DicePanel"""
	def __init__(self, parent, type):
		self.type = type
		self.die = getDie(type)
		self.frame = Frame(parent)
		self.diceCount = getCount(type)

	def makeDice(count):
		return [Die(self.frame, self.type, x) for x in range(count)


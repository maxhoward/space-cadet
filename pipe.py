class pipe:
	def __init__(self, dest):
		self.dest = dest
		self.queue = []

	def push(self, message):
		self.queue.append[message]

	def pop(self):
		out = self.queue[0]
		self.queue = self.queue[1:]
		self.dest.give(out)
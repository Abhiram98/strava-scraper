class actDOwnloader:
	def __init__(self, actIds, jar):
		self.actIds = actIds
		self.jar = jar
		self.done = []

	def fetchAll(self):
		for act in self.actIDs:
			try:
				a = activity(act, self.jar, self.conf)
				a.fetchActivity()
				self.done.append(act)
			except:
				print("Failed to fetch", act)

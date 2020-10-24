class monthIterator:
	def __init__(self, athleteID, browser, conf):
		self.athleteID = athleteID
		self.browser = browser
		self.conf = conf

		self.getNumYears()

	def __iter__(self):
		return self

	def __next__(self):
		# open firefox. go to profile. 
		# Select year
		# Select Month
		# Click month. get all act ids. Channge month, repaeat. Change year repeat.

		
		# self.selectMonthInterval()
		# self.selectMonth()

		return True

	
	def getNumYears(self):
		self.getNumYears = 2
		return 2

	def selectMonthInterval(self):
		timeRange = self.browser.find_element_by_id(self.conf["time_interval_control"])
		self.browser.execute_script("arguments[0].children[0].children[1].children[0].children[1].children[0].click()", timeRange)
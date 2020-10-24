import time

class monthIterator:
	def __init__(self, athleteID, browser, conf):
		self.athleteID = athleteID
		self.browser = browser
		self.conf = conf

		self.getNumYears()
		self.curMonth = 0

	def __iter__(self):
		return self

	def __next__(self):
		# open firefox. go to profile. 
		# Select year
		# Select Month
		# Click month. get all act ids. Channge month, repaeat. Change year repeat.


		# self.selectMonthInterval()
		# self.selectMonth()

		self.getNextMonth()

		return True

	def getNextMonth(self):
		if self.curMonth == 0:
			self.selectMonthInterval()
			self.curMonth+=1
		elif self.curMonth < 13:
			try:
				month = self.browser.find_elements_by_class_name(self.conf['month selection'])[self.curMonth-1]
				self.browser.execute_script("arguments[0].children[0].children[0].click()", month)
				# month.click()
				time.sleep(20)
				self.curMonth+=1

			except IndexError:
				self.curMonth = 13

		else:
			self.curMonth = 0
			self.getNextYear()
			self.selectMonthInterval()
			# raise StopIteration


	def getNextYear(self):
		if self.curYear < self.numYears:
			self.yearSelector = self.browser.find_element_by_id(self.conf["year selector"])
			self.yearSelector.click()

			self.all_years = self.browser.execute_script("return arguments[0].getElementsByTagName('ul')[0].children", self.yearSelector)
			year = self.all_years[self.curYear]
			year.click()
			time.sleep(10)
			
			self.curYear +=1

		else:
			raise StopIteration


	def clickYearDropdown(self):
		self.browser.execute_script("arguments[0].firstChild.click()", self.yearSelector)

	def getNumYears(self):
		
		self.yearSelector = self.browser.find_element_by_id(self.conf["year selector"])
		self.all_years = self.browser.execute_script("return arguments[0].getElementsByTagName('ul')[0].children", self.yearSelector)

		self.numYears = len(self.all_years)
		self.curYear = 0


	def selectMonthInterval(self):
		timeRange = self.browser.find_element_by_id(self.conf["time_interval_control"])
		self.browser.execute_script("arguments[0].children[0].children[1].children[0].children[1].children[0].click()", timeRange)
		time.sleep(10)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time



class monthIterator:
	def __init__(self, athleteID, browser, conf):
		self.athleteID = athleteID
		self.browser = browser
		self.conf = conf

		self.curMonth = 0
		self.curYear = 0
		self.getNumYears()

	def __iter__(self):
		return self

	def __next__(self):
		if self.curMonth==0:
			self.selectMonthInterval()
			self.curMonth+=1
			return True
		elif self.curMonth < 13:
			self.getNextMonth()
			self.curMonth+=1
		else:
			self.curMonth = 0
			self.getNextYear()
			self.curYear+=1
			# self.selectMonthInterval()
		return True

	def getNextMonth(self):
		try:
			firstActivity = self.browser.find_element_by_class_name(self.conf["any activity"])
		except:
			print("No activity found")
			return 
		months = self.browser.find_elements_by_class_name(self.conf['month selection'])
		try:
			months[self.curMonth-1].click()
		except:
			self.curMonth = 13
			self.__next__()
			return 

		#wait for staleness
		try:
		    element = WebDriverWait(self.browser, 100).until(
		        EC.staleness_of(firstActivity)
		    )
		except TimeoutException:
			print("Waited for 100s but nothing happened")
		finally:
		    print("Month Changed")
		    time.sleep(1)

	def getNextYear(self):
		if(self.curYear < self.numYears-1):
			firstActivity = self.browser.find_element_by_class_name(self.conf["any activity"])
			self.year_selector = self.browser.find_element_by_id(self.conf["year selector"])
			self.year_selector.click()
			self.year_selector.find_elements_by_tag_name("li")[self.curYear].click()
			try:
			    element = WebDriverWait(self.browser, 100).until(
			        EC.staleness_of(firstActivity)
			    )
			except TimeoutException:
				print("Waited for 100s but nothing happened")
			finally:
			    print("Year Changed")
			    time.sleep(1)

		else:
			raise StopIteration

	
	def getNumYears(self):
		self.year_selector = self.browser.find_element_by_id(self.conf["year selector"])
		self.numYears = len(self.year_selector.find_elements_by_tag_name("li"))+1

	def selectMonthInterval(self):
		self.weekIntervals = self.browser.find_element_by_class_name(self.conf['month selection'])
		timeRange = self.browser.find_element_by_id(self.conf["time_interval_control"])
		self.browser.execute_script("arguments[0].children[0].children[1].children[0].children[1].children[0].click()", timeRange)
		# Wait for staleness

		try:
		    element = WebDriverWait(self.browser, 100).until(
		        EC.staleness_of(self.weekIntervals)
		    )
		except TimeoutException:
			print("Waited for 100s but nothing happened")
		finally:
		    print("Selected the month range")
		    time.sleep(1)

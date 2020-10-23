from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import requests

import json
import pdb
import time
import random
import sys
import pickle
import os

import sys
sys.path.append("/Users/tubby/Documents/Cycling/Pro-Training-Analysis")

from activity import activity


class stravaExtractor:
	def __init__(self, athleteName, athleteID):

		self.athleteName = athleteName
		self.athleteID = athleteID
		self.cookies = {}

		with open("conf.json") as f:
			self.conf = json.load(f)

		cookies = pickle.load(open("cookies.pkl", "rb"))
		for cookie in cookies:
			if(cookie['name'] in ["strava_remember_token", "strava_remember_id"]):
			    self.cookies[cookie['name']] = cookie


		self.jar = requests.cookies.RequestsCookieJar()
		self.jar.set("strava_remember_id", self.cookies["strava_remember_id"]["value"], domain=self.cookies["strava_remember_id"]["domain"], path='/')
		self.jar.set("strava_remember_token", self.cookies["strava_remember_token"]["value"], domain=self.cookies["strava_remember_token"]["domain"], path='/')

		try:
			os.mkdir(athleteName)
		except:
			print("athlete dir already exists")

		os.chdir(athleteName)

		self.loadAllActivityIds()


	def login(self):
		self.browser = webdriver.Firefox()
		self.browser.get("https://www.strava.com")
		pdb.set_trace()

		pickle.dump(self.browser.get_cookies() , open("cookies.pkl","wb"))

	def loadCookies(self):
		self.browser.get("https://www.strava.com")
		self.browser.add_cookie(self.cookies["strava_remember_id"])
		self.browser.add_cookie(self.cookies["strava_remember_token"])
		# self.browser.get("https://www.strava.com/pros/1126469")

	def openBrowser(self):
		self.browser = webdriver.Firefox()

	def closeBrowser(self):
		self.browser.quit()

	def getActivity(self, actID):
		a = activity(actID)
		a.fetchActivity()
		self.all_ids.append(actID)

	def fetchAllActivities(self):
		self.getAllActivityIds()

		# for id in self.all_ids:
		# 	self.getActivity(id)

	def getNumYears(self):
		return 2

	def selectMonthInterval(self):
		timeRange = self.browser.find_element_by_id(self.conf["time_interval_control"])
		self.browser.execute_script("arguments[0].children[0].children[1].children[0].children[1].children[0].click()", timeRange)

	def selectMonth(self):
		pass

	def getAllActivityIds(self):
		# open firefox. go to profile. 
		# Select year
		# Select Month
		# Click month. get all act ids. Channge month, repaeat. Change year repeat.
		self.openBrowser()
		self.loadCookies()

		self.browser.get("https://www.strava.com"+ self.athleteID)
		time.sleep(2)
		# pdb.set_trace()


		mi = monthIterator(self.athleteID, self.browser)
		# years = self.getNumYears()


		for _ in range(years):
		# for i in mi:
			self.selectMonthInterval()
			time.sleep(2)
			self.selectMonth()
			for ele in self.browser.find_elements_by_class_name(self.conf["solo activity"]):
				href = self.browser.execute_script("return arguments[0].children[1].children[0].href", ele)
				id = href[href.rfind('/')+1:]
				self.all_ids.append(id)

			for ele in self.browser.find_elements_by_class_name(self.conf["group activity"]):
				href = self.browser.execute_script("return arguments[0].getElementsByTagName('li')[0].id", ele)
				id = href[href.find('-')+1:]
				self.all_ids.append(id)


		pdb.set_trace()
		self.closeBrowser()

		with open(self.athleteName+"_all_ids", 'w') as f:
			for i in self.all_ids:
				f.write(i+"\n")


	def loadAllActivityIds(self):

		try:
			with open(self.athleteName+"_all_ids", 'r') as f:
				self.all_ids = f.read().split('\n')
				self.all_ids = list(set(self.all_ids))

		except:
			print(self.athleteName+"_all_ids file not present")
			self.all_ids = []

class monthIterator:
	def __init__(self, athleteID, browser):
		self.athleteID = athleteID
		self.browser = browser

	def __iter__(self):
		return self

	def __next__(self):


		

# def tryThis():

# 	# pdb.set_trace()

def main():
	# tryThis()
	se = stravaExtractor("Alex Dowsett", "/pros/505408")
	se.fetchAllActivities()

	# se.getActivity("3842740325")


if __name__ == "__main__":
	main()
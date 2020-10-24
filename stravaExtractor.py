from selenium import webdriver
import requests
import json
import pdb
import time
import random
import sys
import pickle
import os

from monthIterator import monthIterator


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

	def getAllActivityIds(self):
		
		self.openBrowser()
		self.loadCookies()

		self.browser.get("https://www.strava.com"+ self.athleteID)
		time.sleep(2)
		# pdb.set_trace()


		mi = monthIterator(self.athleteID, self.browser, self.conf)


		for i in mi:
			# self.selectMonthInterval()
			
			# self.selectMonth()
			time.sleep(2)
			for ele in self.browser.find_elements_by_class_name(self.conf["solo activity"]):
				href = self.browser.execute_script("return arguments[0].children[1].children[0].href", ele)
				id = href[href.rfind('/')+1:]
				self.all_ids.append(id)

			for ele in self.browser.find_elements_by_class_name(self.conf["group activity"]):
				href = self.browser.execute_script("return arguments[0].getElementsByTagName('li')[0].id", ele)
				id = href[href.find('-')+1:]
				self.all_ids.append(id)


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



		
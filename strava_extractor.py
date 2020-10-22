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


class activity:
	def __init__(self, actID, jar, conf):
		self.actID = actID
		self.jar = jar
		self.conf = conf

	
	def fetchActivity(self):
		self.getOverview()
		self.processOverview()
		self.getPowerSummary()
		self.getLapData()
		self.getStreamData()


	def getOverview(self):
		url = 'https://www.strava.com/activities/'+self.actID+'/overview'
		response = requests.get(url, cookies=self.jar)

		self.date_and_time  = response.text[response.text.find("<time>")+len("<time>")+1: response.text.find("</time>") - 1]
		self.date = self.date_and_time[self.date_and_time.find(',')+1:]
		self.html = response.text
		self.dir = self.date + " - " + self.actID
		try:
			os.mkdir(self.dir)
		except:
			print("File already loaded. Skipping")

	def processOverview(self):
		try:
			with open(os.path.join(self.dir, self.actID+"_overview.html"), "w") as f:
				f.write(self.html)
		except:
			print("Failed to write overview for", self.actID)

	def getPowerSummary(self):
		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["power_summary"]
		response = requests.get(url, cookies=self.jar)
		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_power_summary"), "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch power summary for", self.actID)

	def getLapData(self):
		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["lap_summary"]
		response = requests.get(url, cookies=self.jar)
		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_lap_summary"), "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch lap data for", self.actID)

	def getStreamData(self):
		# pdb.set_trace()

		url = 'https://www.strava.com/activities/'+self.actID+'/streams'
		payload = {self.conf["stream_name"]: self.conf["streams"]}
		response = requests.get(url, cookies=self.jar, params = payload)
		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_streams"), "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch streams for", self.actID)


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
		self.browser = webdriver.Firefox()
		self.browser.get("https://www.strava.com")
		self.browser.add_cookie(self.cookies["strava_remember_id"])
		self.browser.add_cookie(self.cookies["strava_remember_token"])
		# self.browser.get("https://www.strava.com/pros/1126469")

	def closeBrowser(self):
		self.browser.quit()

	def getActivity(self, actID):
		a = activity(actID)
		a.fetchActivity()
		self.all_ids.append(actID)

	def fetchAllActivities(self):
		self.getAllActivityIds()

		for id in self.all_ids:
			self.getActivity(id)

	def getAllActivityIds(self):
		# open firefox. go to profile. Click month. get all act ids. Channge month, repaeat. Change year repeat.
		self.loadCookies()


	def loadAllActivityIds(self):

		try:
			with open(self.athleteName+"_all_ids", 'r') as f:
				self.all_ids = json.load(f)

		except:
			print(self.athleteName+"_all_ids file not present")
			self.all_ids = []

		
		

# def tryThis():

# 	# pdb.set_trace()

def main():
	# tryThis()
	se = stravaExtractor("Alex Dowsett", "/pros/505408")
	se.fetchAllActivities()

	# se.getActivity("3842740325")


if __name__ == "__main__":
	main()
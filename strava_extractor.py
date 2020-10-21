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




class stravaExtractor:
	def __init__(self, athleteName, athleteID):
		# self.cred = cred
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
		self.browser.get("https://www.strava.com/pros/1126469")

	def closeBrowser(self):
		self.browser.quit()

	def getPowerSummary(self, actID):
		url = 'https://www.strava.com/activities/'+actID+'/'+self.conf["power_summary"]
		response = requests.get(url, cookies=self.jar)
		try:
			js = response.json()
			with open(actID+"_power_summary", "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch power summary for", actID)
	
	def getLapData(self, actID):
		url = 'https://www.strava.com/activities/'+actID+'/'+self.conf["lap_summary"]
		response = requests.get(url, cookies=self.jar)
		try:
			js = response.json()
			with open(actID+"_lap_data", "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch lap data for", actID)
	
	def getStreamData(self, actID):
		pdb.set_trace()

		url = 'https://www.strava.com/activities/'+actID+'/streams'
		payload = {self.conf["stream_name"]: self.conf["streams"]}
		response = requests.get(url, cookies=self.jar, params = payload)
		try:
			js = response.json()
			with open(actID+"_streams", "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch streams for", actID)
	

	def getActivity(self, actID):
		# self.getPowerSummary(actID)
		# self.getLapData(actID)
		self.getStreamData(actID)

		
		
		

# def tryThis():

# 	# pdb.set_trace()

def main():
	# tryThis()
	se = stravaExtractor("Alex Dowsett", "1234")
	# # se.login()
	# se.loadCookies()
	# se.closeBrowser()
	se.getActivity("3842740325")


if __name__ == "__main__":
	main()
from selenium import webdriver
import requests
import json
import pdb
import time
import random
import sys
import pickle
import os
import threading
import csv
import pandas as pd

from monthIterator import monthIterator
from activity import activity
from dirSummary import dirSummary


class stravaExtractor:
	def __init__(self, athleteName = None, athleteID = None):
		if (athleteName==None and athleteID == None):
			print("No name and athlete id provided. Exiting")
			return
		self.athleteName = athleteName
		self.athleteID = athleteID
		self.cookies = {}
		print("Current wd - ", os.getcwd())
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
		input("Hit Return after logging in to strava on the browser that pops up")

		pickle.dump(self.browser.get_cookies() , open("Data and Scraping/"+"cookies.pkl","wb"))

	def loadCookies(self):
		self.browser.get("https://www.strava.com")
		self.browser.add_cookie(self.cookies["strava_remember_id"])
		self.browser.add_cookie(self.cookies["strava_remember_token"])
		# self.browser.get("https://www.strava.com/pros/1126469")

	def openBrowser(self):
		self.browser = webdriver.Firefox()

	def closeBrowser(self):
		self.browser.quit()


	def fetchAllActivities(self):
		# self.getAllActivityIds()
		print("Fetching")
		self.createMapFile()
		numThreads = 10
		threads = []
		l = len(self.all_ids)

		for i in range(numThreads):

			x = threading.Thread(target=stravaExtractor.sender, args=(self.all_ids[int(i*l/numThreads):int((i+1)*l/numThreads)], self.jar, self.conf, self.athleteName, ))
			x.start()
			threads.append(x)

		for i in range(numThreads):
			threads[i].join()

		self.delete_duplicates_map()

		print("all done.")

	def sender(acts, jar, conf, athleteName):
		for i in acts:
			a = activity(i, jar, conf, athleteName)
			a.fetchActivity()

	def getSelectMonths(self):
		self.openBrowser()
		self.loadCookies()

		self.browser.get("https://www.strava.com"+ self.athleteID)
		time.sleep(2)

		ip = input("Get more months(y/n)")
		# for i in mi:
		while ip == 'y':
			for ele in self.browser.find_elements_by_class_name(self.conf["solo activity"]):
				href = self.browser.execute_script("return arguments[0].children[1].children[0].href", ele)
				id = href[href.rfind('/')+1:]
				self.all_ids.append(id)

			for ele in self.browser.find_elements_by_class_name(self.conf["group activity"]):
				href = self.browser.execute_script("return arguments[0].getElementsByTagName('li')[0].id", ele)
				id = href[href.find('-')+1:]
				self.all_ids.append(id)

			ip = input("Get more months(y/n)")	

		self.closeBrowser()

		with open(self.athleteName+"_all_ids", 'w') as f:
			for i in self.all_ids:
				f.write(i+"\n")


	def getAllActivityIds(self):
		
		self.openBrowser()
		self.loadCookies()

		self.browser.get("https://www.strava.com"+ self.athleteID)
		time.sleep(2)
		# pdb.set_trace()


		mi = monthIterator(self.athleteID, self.browser, self.conf)

		try:
			for i in mi:
				for ele in self.browser.find_elements_by_class_name(self.conf["solo activity"]):
					href = self.browser.execute_script("return arguments[0].children[1].children[0].href", ele)
					id = href[href.rfind('/')+1:]
					self.all_ids.append(id)

				for ele in self.browser.find_elements_by_class_name(self.conf["group activity"]):
					href = self.browser.execute_script("return arguments[0].getElementsByTagName('li')[0].id", ele)
					id = href[href.find('-')+1:]
					self.all_ids.append(id)
		except:
			print("failed at some point.")


		self.closeBrowser()

		with open(self.athleteName+"_all_ids", 'w') as f:
			for i in self.all_ids[:-1]:
				f.write(i+"\n")
			f.write(self.all_ids[-1])


	def loadAllActivityIds(self):

		try:
			with open(self.athleteName+"_all_ids", 'r') as f:
				self.all_ids = f.read().split('\n')
				self.all_ids = list(set(self.all_ids))

		except:
			print(self.athleteName+"_all_ids file not present")
			self.all_ids = []

	def getDirSummary(self):
		os.chdir("..")
		d = dirSummary(self.athleteName)
		d.get()
		os.chdir(self.athleteName)

	def createMapFile(self):
		try:
			open(self.athleteName+"_map.csv", 'r')
			print("_map file exists")
		except:
			print("creating _map.csv")
			f = open(self.athleteName+"_map.csv", 'w')
			fieldnames = ["ID", "Title", "Acitvity Type", "Date", "Time", "Distance","Moving Time"]
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer.writeheader()
			f.close()


	def delete_duplicates_map(self):
		# df = pd.read_csv(self.athleteName+"_map.csv")
		# if len(set(df.ID)) != len(df):
		# 	print("deleting duplicates from _map")
		pass

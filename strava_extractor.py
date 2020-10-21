from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import json
import pdb
import time
import random
import sys
import pickle




class stravaExtractor:
	def __init__(self, athleteName, athleteID):
		# self.cred = cred
		self.browser = webdriver.Firefox()



	def login(self):
		self.browser.get("https://www.strava.com")
		pdb.set_trace()

		pickle.dump(self.browser.get_cookies() , open("cookies.pkl","wb"))

	def loadCookies(self):
		self.browser.get("https://www.strava.com")
		cookies = pickle.load(open("cookies.pkl", "rb"))
		for cookie in cookies:
			if(cookie['name'] in ["strava_remember_token", "strava_remember_id"]):
			    self.browser.add_cookie(cookie)
		self.browser.get("https://www.strava.com/pros/1126469")

	def closeBrowser(self):
		self.browser.quit()


# def tryThis():

# 	# pdb.set_trace()

def main():
	# tryThis()
	se = stravaExtractor("Alex Dowsett", "1234")
	# # se.login()
	se.loadCookies()


if __name__ == "__main__":
	main()
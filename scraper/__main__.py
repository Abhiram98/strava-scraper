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
import argparse
import sys
from datetime import datetime

#helper imports
from activity import activity
from stravaExtractor import stravaExtractor


def main():

	desc = """
	To scrape athlete data from strava.

	Run 'collect' to collect all activity ids from an athlete
	
	Run 'download' to attempt to download all activities from an athlete

	Run 'overview' to synthesise the overview of an athlete

	Run 'login' to login to your strava account. Please use the remember me feature to save your login cookies. 


	"""
	my_parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.RawDescriptionHelpFormatter)

	my_parser.add_argument('command', metavar='comm', type=str, help='Command')
	# my_parser.add_argument('func_name', metavar='func', type=str, help='Analysis function on athlete. Possibilities - get_power_hist, get_hr_hist')
	my_parser.add_argument('-name', '--name', type=str, help='Name of athlete')
	my_parser.add_argument('-i', '--id', type=str, help='Id of athlete')
	my_parser.add_argument('-s', '--select', type=str, help='To select particular months to collect Ids from (0/1)', default ='0')
	args = vars(my_parser.parse_args())

	print("Start Time", datetime.now())

	if args['command'] == "login":
		se = stravaExtractor()
		se.login()


	athleteName = args['name']
	athleteID = args['id']
	# se = stravaExtractor("Alex Dowsett", "/pros/505408")
	se = stravaExtractor(athleteName, athleteID)
	if(args['command'] == "download"):
		se.fetchAllActivities()
	elif(args['command'] == "collect"):
		if args['select'] == '1':
			se.getSelectMonths()
		else:
			se.getAllActivityIds()
	elif (args['command'] == "overview"):
		se.getDirSummary()
	else:
		raise Exception("Command does not exist")

	print("End time", datetime.now())
if __name__ == "__main__":
	main()
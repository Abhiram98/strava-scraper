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
sys.path.append(".")

from stravaExtractor import stravaExtractor



# def tryThis():

# 	# pdb.set_trace()

def main():
	# tryThis()
	se = stravaExtractor("Alex Dowsett", "/pros/505408")
	se.fetchAllActivities()

	# se.getActivity("3842740325")


if __name__ == "__main__":
	main()
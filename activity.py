import requests
import os
import json
class activity:
	overviewBad = False
	power_summaryBad = False
	streamsBad = False
	lap_summaryBad = False

	def __init__(self, actID, jar, conf):
		self.actID = actID
		self.jar = jar
		self.conf = conf
		self.someLoaded = False

	
	def fetchActivity(self):
		self.dir = actID
		try:
			os.mkdir(self.dir)
		except FileExistsError:
			# print("Files already loaded. Skipping", self.actID)
			self.someLoaded = True


		if !overviewBad:
			self.getOverview()
		if !power_summaryBad:
			self.getPowerSummary()
		if !lap_summaryBad:
			self.getLapData()
		if !streamsBad:
			self.getStreamData()


	def getOverview(self):
		if self.someLoaded:
			try:
				open(os.path.join(self.dir, self.actID+"_overview.html"), "r")
				return
			except FileNotFoundError:
				pass

		url = 'https://www.strava.com/activities/'+self.actID+'/overview'
		response = requests.get(url, cookies=self.jar)
		if(response.status_code == 429):
			overviewBad = True
			return 

		self.date_and_time  = response.text[response.text.find("<time>")+len("<time>")+1: response.text.find("</time>") - 1]
		self.date = self.date_and_time[self.date_and_time.find(',')+1:]
		self.html = response.text
		self.processOverview()
		# self.dir = self.date + " - " + self.actID

	def processOverview(self):
		try:
			with open(os.path.join(self.dir, self.actID+"_overview.html"), "w") as f:
				f.write(self.html)
		except Exception as e:
			print("Failed to write overview for", self.actID)
			print(e)

	def getPowerSummary(self):
		if self.someLoaded:
			try:
				open(os.path.join(self.dir, self.actID+"_power_summary"), "r")
				return
			except FileNotFoundError:
				pass

		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["power_summary"]
		response = requests.get(url, cookies=self.jar)
		if(response.status_code == 429):
			power_summaryBad = True
			return 
		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_power_summary"), "w") as f:
				json.dump(js, f)
		except Exception as e:
			print("Failed to fetch power summary for", self.actID)
			print(e)

	def getLapData(self):
		if self.someLoaded:
			try:
				open(os.path.join(self.dir, self.actID+"_lap_summary"), "r")
				return
			except FileNotFoundError:
				pass

		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["lap_summary"]
		response = requests.get(url, cookies=self.jar)
		if(response.status_code == 429):
			lap_summaryBad = True
			return 

		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_lap_summary"), "w") as f:
				json.dump(js, f)
		except Exception as e:
			print("Failed to fetch lap data for", self.actID)
			print(e)

	def getStreamData(self):
		# pdb.set_trace()
		if self.someLoaded:
			try:
				open(os.path.join(self.dir, self.actID+"_streams"), "r")
				return
			except FileNotFoundError:
				pass
		
		url = 'https://www.strava.com/activities/'+self.actID+'/streams'
		payload = {self.conf["stream_name"]: self.conf["streams"]}
		response = requests.get(url, cookies=self.jar, params = payload)
		if(response.status_code == 429):
			streamsBad = True
			return 

		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_streams"), "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch streams for", self.actID)


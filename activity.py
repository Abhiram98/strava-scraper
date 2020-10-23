import requests


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


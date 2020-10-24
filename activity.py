import requests


class activity:
	overviewBad = False
	power_summaryBad = False
	streamsBad = False
	lap_summaryBad = False

	def __init__(self, actID, jar, conf):
		self.actID = actID
		self.jar = jar
		self.conf = conf

	
	def fetchActivity(self):
		self.dir = actID
		try:
			os.mkdir(self.dir)
		except FileExistsError:
			# print("Files already loaded. Skipping", self.actID)
			self.someLoaded = True


		if overviewBad==False:
			self.getOverview()
		if power_summaryBad==False:
			self.getPowerSummary()
		if lap_summaryBad==False:
			self.getLapData()
		if streamsBad==False:
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
		except:
			print("Failed to write overview for", self.actID)

	def getPowerSummary(self):
		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["power_summary"]
		response = requests.get(url, cookies=self.jar)
		if(response.status_code == 429):
			power_summaryBad = True
			return 
		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_power_summary"), "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch power summary for", self.actID)

	def getLapData(self):
		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["lap_summary"]
		response = requests.get(url, cookies=self.jar)
		if(response.status_code == 429):
			lap_summaryBad = True
			return 

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
		if(response.status_code == 429):
			streamsBad = True
			return 

		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_streams"), "w") as f:
				json.dump(js, f)
		except:
			print("Failed to fetch streams for", self.actID)


import requests
import os
import json
from bs4 import BeautifulSoup
import csv

class activity:

	overviewBad = False
	power_summaryBad = False
	lap_summaryBad = False
	streamsBad = False

	def __init__(self, actID, jar, conf, athlete_name):
		self.actID = actID
		self.jar = jar
		self.conf = conf
		self.athlete_name = athlete_name
		self.someLoaded = False

	
	def fetchActivity(self):
		self.dir = self.actID
		try:
			os.mkdir(self.dir)
		except FileExistsError:
			# print("Files already loaded. Skipping", self.actID)
			self.someLoaded = True


		if activity.overviewBad==False:
			self.getOverview()
		if activity.power_summaryBad==False:
			self.getPowerSummary()
		if activity.lap_summaryBad==False:
			self.getLapData()
		if activity.streamsBad==False:
			self.getStreamData()


	def getOverview(self):

		if self.someLoaded:
			try:
				f = open(os.path.join(self.dir, self.actID+"_overview.html"), "r")
				return 
			except FileNotFoundError:
				pass

		url = 'https://www.strava.com/activities/'+self.actID+'/overview'
		response = requests.get(url, cookies=self.jar)

		if response.status_code == 429:
			activity.overviewBad = True
			return 

		if response.status_code == 404:
			with open(os.path.join(self.dir, self.actID+"_overview.html"), "w") as f:
				f.write("No Data")
			return

		self.date_and_time  = response.text[response.text.find("<time>")+len("<time>")+1: response.text.find("</time>") - 1]
		self.date = self.date_and_time[self.date_and_time.find(',')+1:]
		self.html = response.text
		# self.dir = self.date + " - " + self.actID
		self.processOverview()

	def processOverview(self):


		try:
			with open(os.path.join(self.dir, self.actID+"_overview.html"), "w") as f:
				f.write(self.html)
			print("Fetched overview for", self.actID)
			self.processHtml()
		except Exception as e:
			print("Failed to write overview for", self.actID)
			print(e)
			print()

			with open(os.path.join(self.dir, self.actID+"_overview.html"), "w") as f:
				f.write("No Data")
			return

	def processHtml(self):
		with open(os.path.join(self.dir,  self.actID+"_overview.html"), "r") as f:
			try:
				try:
					f3 = open(os.path.join(self.dir, self.actID+"_overview.json"), "r")
					return
				except FileNotFoundError:
					pass

				soup = BeautifulSoup(f, "html.parser")
				# pdb.set_trace()

				complete_time = soup.find("time").text[1:]
				date = complete_time[complete_time.find(",")+2:].replace('\n','')
				time = complete_time[:complete_time.find(",")].replace('\n','')

				basic_stats = soup.find("ul", class_="inline-stats section")
				basic_stats_data = {}
				for i in basic_stats.find_all("li"):
					ind = i.find('div').text
					ind = ind.replace('\n','')
					basic_stats_data[ind] = i.find('strong').text.replace('\n','')

				sec_stats = soup.find("ul", class_ = "inline-stats section secondary-stats")
				sec_stats_data = {}

				try:
					for i in sec_stats.find_all('li'):
						ind = i.find('div').text
						ind = ind.replace('\n','')
						sec_stats_data[ind] = i.find('strong').text.replace('\n','')
				except:
					print("No secondary-stats for", self.actID)

				more_stats_data = {}
				try:
					more_stats = soup.find('div', class_ = "section more-stats")
					for i in more_stats.find_all('tr')[1:]:
						data = i.find_all("td")
						avg = data[0].text.replace('\n','')
						max = None

						if(len(data) > 1):
							max = data[1].text.replace('\n','')

						more_stats_data[i.find("th").text.replace('\n','')] = {"Avg": avg, "Max": max}
				except:
					print("No more_stats for", self.actID)

				try:
					device = soup.find("div", class_="section device-section").text[3:-3]
				except:
					print("No device found for", self.actID)


				# pdb.set_trace()

				title = soup.find(class_='activity-name').text.replace('\n','')
				act_type = soup.find('span',class_='title').text
				act_type = act_type[act_type.find('–')+1:].replace('\n','')


				all_stats = {
					"Title":title,
					"Acitvity Type": act_type, 
					"Date": date,
					"Time": time,
					"Basic Stats": basic_stats_data,
					"Secondary Stats": sec_stats_data,
					"More Stats": more_stats_data
				}

				with open(os.path.join(self.dir, self.actID+"_overview.json"), "w")as f2:
					json.dump(all_stats, f2)

				self.write_to_map(all_stats)
			except Exception as e:
				print("Failed to process html_overview for", self.actID, "error:", e)	



	def getPowerSummary(self):
		
		if self.someLoaded:
			try:
				f = open(os.path.join(self.dir, self.actID+"_power_summary.json"), "r")
				return 
			except FileNotFoundError:
				pass


		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["power_summary"]
		response = requests.get(url, cookies=self.jar)

		if response.status_code == 429:
			activity.power_summaryBad = True
			return 
		if response.status_code == 404:
			with open(os.path.join(self.dir, self.actID+"_power_summary.json"), "w") as f:
				f.write("No Data")
			return

		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_power_summary.json"), "w") as f:
				json.dump(js, f)
			print("Fetched power_summary for", self.actID)
		except Exception as e:
			print("Failed to fetch power summary for", self.actID)
			print(e)
			print()

			with open(os.path.join(self.dir, self.actID+"_power_summary.json"), "w") as f:
				f.write("No Data")
			return

	def getLapData(self):

		if self.someLoaded:
			try:
				f = open(os.path.join(self.dir, self.actID+"_lap_summary.json"), "r")
				return 
			except FileNotFoundError:
				pass

		url = 'https://www.strava.com/activities/'+self.actID+'/'+self.conf["lap_summary"]
		response = requests.get(url, cookies=self.jar)

		if response.status_code == 429:
			activity.lap_summaryBad = True
			return 
		if response.status_code == 404:
			with open(os.path.join(self.dir, self.actID+"_lap_summary.json"), "w") as f:
				f.write("No Data")
			return
		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_lap_summary.json"), "w") as f:
				json.dump(js, f)
			print("Fetched lap_summary for", self.actID)
		except Exception as e:
			print("Failed to fetch lap data for", self.actID)
			print(e)
			print()

			with open(os.path.join(self.dir, self.actID+"_lap_summary.json"), "w") as f:
				f.write("No Data")
			return

	def getStreamData(self):
		# pdb.set_trace()
		if self.someLoaded:
			try:
				f = open(os.path.join(self.dir, self.actID+"_streams.json"), "r")
				return 
			except FileNotFoundError:
				pass

		url = 'https://www.strava.com/activities/'+self.actID+'/streams'
		payload = {self.conf["stream_name"]: self.conf["streams"]}
		response = requests.get(url, cookies=self.jar, params = payload)
		
		if response.status_code == 429:
			activity.streamsBad = True
			return 

		if response.status_code == 404:
			with open(os.path.join(self.dir, self.actID+"_streams.json"), "w") as f:
				f.write("No Data")
			return

		try:
			js = response.json()
			with open(os.path.join(self.dir, self.actID+"_streams.json"), "w") as f:
				json.dump(js, f)
			print("Fetched streams for", self.actID)
		except Exception as e:
			print("Failed to fetch streams for", self.actID)
			print(e)
			print()
			with open(os.path.join(self.dir, self.actID+"_streams.json"), "w") as f:
				f.write("No Data")
			return

	def write_to_map(self, over):
		try:
			time = over["Basic Stats"]["Moving Time"]
		except KeyError:
			try:
				time = over["Basic Stats"]["Elapsed Time"]
			except KeyError:
				time = over["Basic Stats"]["Duration"]

		# self.file.write(dir+",\""+over["Title"]+"\",\""+over["Acitvity Type"]+"\",\""+over["Date"]+"\",\""+over["Time"]+"\","+over["Basic Stats"]["Distance"]+","+time+"\n")

		f = open(os.path.join("..", self.athlete_name+"_map.csv"), "a")
		fieldnames = ["ID", "Title", "Acitvity Type", "Date", "Time", "Distance","Moving Time"]
		writer = csv.DictWriter(f, fieldnames=fieldnames)
		writer.writerow({"ID":self.actID,  "Title":over["Title"], "Acitvity Type":over["Acitvity Type"] , "Date":over["Date"], "Time":over["Time"], "Distance":over["Basic Stats"]["Distance"],"Moving Time":time})
		f.close()

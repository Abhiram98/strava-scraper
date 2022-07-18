import os
import json
import csv

class dirSummary:
	def __init__(self, dirName):
		self.dirName = dirName
		self.file = open(os.path.join(self.dirName, self.dirName+"_map.csv"), "w")
		fieldnames = ["ID", "Title", "Acitvity Type", "Date", "Time", "Distance","Moving Time"]
		self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
		self.writer.writeheader()

	def get(self):

		for subdir, dirs, files in os.walk(self.dirName):
			for dir in dirs:
				for subdir2, dirs2, files2 in os.walk(os.path.join(self.dirName,dir)):
					print(files2)
					if dir+"_overview.json" in files2:
						with open(os.path.join(self.dirName,dir,dir+"_overview.json"),'r') as f:
							over = json.load(f)
							try:
								time = over["Basic Stats"]["Moving Time"]
							except KeyError:
								try:
									time = over["Basic Stats"]["Elapsed Time"]
								except KeyError:
									time = over["Basic Stats"]["Duration"]

							# self.file.write(dir+",\""+over["Title"]+"\",\""+over["Acitvity Type"]+"\",\""+over["Date"]+"\",\""+over["Time"]+"\","+over["Basic Stats"]["Distance"]+","+time+"\n")
							self.writer.writerow({"ID":dir,  "Title":over["Title"], "Acitvity Type":over["Acitvity Type"] , "Date":over["Date"], "Time":over["Time"], "Distance":over["Basic Stats"]["Distance"],"Moving Time":time})


if __name__ == "__main__":
	d = dirSummary("./Robert Gesink")
	d.get()




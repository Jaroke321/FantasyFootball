import requests
from bs4 import BeautifulSoup

class Defense(object):
	'''This class represents a Defensive team in the NFL'''

	####################################################
	# Declare all class level variables here
	####################################################

	# Holds all of the defense category labels that are gathered
	Alldata = {}  # Passing, Rushing, Scoring
	# Holds all of the teams and some relevant stats for their offenses
	offenseRankings = {}

	# Store all links used for defenses here
	offenseLink = "https://www.espn.com/nfl/stats/team"
	defenseLink = "https://www.nfl.com/stats/team-stats/defense/{0}/2020/reg/all"
	scheduleLink = "https://www.espn.com/nfl/team/schedule/_/name/{0}"

	def __init__(self, name):

		# Initialize all of the variables used for an individual defense
		self.team = name    # Holds the name of the team
		self.data = []      # Holds all of the relevant data for this defense
		self.schedule = []  # Holds all of the teams this defense has faced
		self.opponent = ""  # Holds the name of the opponent the defense is facing
		self.score = 0      # Holds the Fantasy score of the defense

	def getData(self, dir):
		'''This method is used to make the HTTP request to the website
		in order to get the appropriate data. The data gathered will be both
		the passing defense and the rushing defense statistics.'''

		# Make all three of the links
		passLink = Defense.defenseLink.format("passing")
		rushLink = Defense.defenseLink.format("rushing")
		scoreLink = Defense.defenseLink.format("scoring")

		# Make the requests to get the webpage
		passPage = requests.get(passLink)
		rushPage = requests.get(rushLink)
		scorePage = requests.get(scoreLink)

		# Make the files to store the webpages in
		passFile = open("{0}/{1}.html".format(dir, "passing_defense_stats"), "w")
		rushFile = open("{0}/{1}.html".format(dir, "rushing_defense_stats"), "w")
		scoreFile = open("{0}/{1}.html".format(dir, "scoring_defense_stats"), "w")

		# Write data to the file
		passFile.write(passPage.text)
		rushFile.write(rushPage.text)
		scoreFile.write(scorePage.text)

		# Close all three files
		passFile.close()
		rushFile.close()
		scoreFile.close()

		# Start with the Pass Ranking
		with open("{0}/{1}.html".format(dir, "passing_defense_stats"), "r") as f:
			# Create a Beautiful soup object
			soup = BeautifulSoup(f.read(), 'html.parser')
			# Get the data categories first
			cat = soup.thead.tr.find_all('th')
			cat_pass = [c.text for c in cat]

			# Append the pass categories to the dataCategories class variable
			Defense.Alldata["passing_categories"] = cat_pass

			# Get this teams passing stats
			rows = soup.find_all('tr')[1:]
			# Go through each row until this team is found
			for r in rows:
				
				tds = r.find_all('td')    # Seperates each column in the row

				# Get the name of the current team
				name = tds[0].find('div', class_ = "d3-o-club-fullname").text.strip()
				# initialize this teams data with an  empty array
				Defense.Alldata[name] = []
				# Go through each column and append the data to the team array
				team_arr = [ d.text.strip() for d in tds[1:] ]
				# Add the current teams passing data to the data dictionary
				Defense.Alldata[name].append(team_arr)

		# Extract data from the rush File as well
		with open("{0}/{1}.html".format(dir, "rushing_defense_stats"), "r") as f:
			# Create a Beautiful Soup Object
			soup = BeautifulSoup(f.read(), 'html.parser')
			# Get the data categories first
			cat = soup.thead.tr.find_all('th')
			cat_rush = [c.text for c in cat]

			# Append the pass categories to the dataCategories class variable
			Defense.Alldata["rushing_categories"] = cat_rush

			# Get this teams rushing stats
			rows = soup.find_all('tr')[1:]
			# Go through each row of data
			for r in rows:
				# Search once for all td elements in this row
				tds = r.find_all('td')
				# Get the name from the first element
				name = tds[0].find('div', class_="d3-o-club-fullname").text.strip()
				# Go through each column and get the rushing data for the team
				team_arr = [ d.text.strip() for d in tds[1:] ]
				# Add the rushing data to the allData dictionary
				Defense.Alldata[name].append(team_arr)


	def getSchedule(self, dir):
		'''This method will gather the different offenses that have been faced
		by this defense up until this point in the season.'''

		# List of odd naming conventions used by ESPN
		odd = ["Los Angeles Rams", "Los Angeles Chargers", "New York Giants",
			"New York Jets"]
		# Split the name to seperate the city from the team
		name = self.team.split()

		# Get the correct parameter for the link based on team name
		if(self.team in odd):
			# Grab the first letter from each of the words in name for link
			param = (name[0][0] + name[1][0] + name[2][0]).lower()
		elif(len(self.team.split()) == 3):
			# Just grab the first letter of the first two words for link
			param = (name[0][0] + name[1][0]).lower()
		else:
			# Grab the first three letters of the first word for link
			param = name[0][0:3].lower()

		# Create the link to use
		link = Defense.scheduleLink.format(param)
		# Make the request to the website
		webpage = requests.get(link)
		# Create the file
		file = open("{0}/{1}.html".format(dir, self.team + "_schedule"), "w")
		# Write the html webpage to the file
		file.write(webpage.text)
		file.close()   # Close the file

		# Open the file and extract the schedule data
		with open("{0}/{1}.html".format(dir, self.team + "_schedule"), "r") as f:
			# Create a BeautifulSoup object
			soup = BeautifulSoup(f.read(), 'html.parser')
			# Get each game as a row
			rows = soup.find_all('tr', class_="Table__TR--sm")[2:]
			# Create a count variable to keep track of the current row
			count = 0
			# Go through each row and find the opponent of that week
			for r in rows:
				count += 1 # Increment the count variable
				# Seperate each row by its columns
				cols = r.find_all('td')
				if(len(cols) == 8): # Game was played this week
					# Gather the opponent name
					ans = " ".join([c.capitalize() for c in r.a.get('href').split("/")[-1].split("-")])
					self.schedule.append(ans)

				elif(len(cols) == 6): # Column of length 6 is the next games row
					# Get the upcoming opponent
					self.opponent = " ".join([c.capitalize() for c in rows[count].a.get('href').split("/")[-1].split("-")])
					# Break out of the loop, data has been gathered
					break


	def calculateScore(self):
		'''This method will calculate the score associated with this defense
		using all of the data gathered. This score represents the value of
		this defense for the mathcup this week of the season.'''

		avg_off = [0.0, 0.0, 0.0, 0.0]                    # Used to store the average offenses
		cur_off = Defense.offenseRankings[self.opponent]  # Used to get the stats of this weeks offense

		# Get the average offense faced by this defense
		for team in self.schedule:
			# Grab the teams stats from the offense rankings
			stats = Defense.offenseRankings[team]
			# Go through each stat and add them to the avg_off array
			for i in range(len(stats)):
				avg_off[i] += float(stats[i])

		# Divide each value in the average array by the number of games played
		for i in range(len(avg_off)):
			avg_off[i] /= len(self.schedule)

		# Get the difference between the average and the current offenses
		diff = [float(cur_off[i]) - avg_off[i] for i in range(4)]


	def printDefense(self):
		'''This method displays all of the current data on the defense'''

		# Print the teams name first
		print("\nDEFENSE: " + self.team)
		print("This weeks Opponent: " + self.opponent + "\n")

		# Print passing stats
		print("Passing Stats:\n")
		for i in range(len(Defense.dataCategories[0]) - 1):
			print("\t" + Defense.dataCategories[0][i+1] + " -> " + self.data[0][i])

		# Print the rushing stats second
		print("\nRushing Stats:\n")
		for i in range(len(Defense.dataCategories[1]) - 1):
			print("\t" + Defense.dataCategories[1][i+1] + " -> " + self.data[1][i])

		print()

		# Print all opponents up until this point
		print("Opponents faced:\n")
		for o in self.schedule:
			print("\t-> " + o)

##############################################################
# STATIC METHODS
##############################################################

	@staticmethod
	def printOffenseData():
		'''This method will print out the offense rankings dictionary class
		variable in a readable manner to the console.'''

		for k, v in Defense.offenseRankings.items():
			print(k + ":\n")
			print("   --> Total yds/g: {0} , Passing yds/g: {1} , Rushing yds/g: {2} , Points/g : {3}"
				.format(v[0], v[1], v[2], v[3]))
			print()

	@staticmethod
	def getOffenseRankings(dir):
		'''This method will gather all of the teams in the league and some of
		the general data that is associated with their offenses. This data will
		then be stored in the class variable, offenseRankings.'''

		# Make the web request to get the html
		webpage = requests.get(Defense.offenseLink)
		# Create the file and write the page to it
		file = open("{0}/{1}.html".format(dir, "espn_offenses"), "w")
		file.write(webpage.text)
		file.close()

		# Open the file and extract the appropriate data
		with open("{0}/{1}.html".format(dir, "espn_offenses"), "r") as f:
			# Create a BeautifulSoup object
			soup = BeautifulSoup(f.read(), 'html.parser')
			data = soup.find_all('tr', class_ = 'Table__TR--sm')

			# Go through once for each NFL team and get the data and team name
			for i in range(32):
				# Get team name
				team = data[i].text
				temp_list = []  # Holds all of the data
				# Get all of the div elements from the html
				temp_data = data[i + 32].find_all('div')
				# Add the correct columns to the list
				temp_list.append(temp_data[2].text)
				temp_list.append(temp_data[4].text)
				temp_list.append(temp_data[6].text)
				temp_list.append(temp_data[8].text)
				# Add the list to the dictionary with the team name as key
				Defense.offenseRankings[team] = temp_list

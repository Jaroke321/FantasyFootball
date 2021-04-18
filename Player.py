import requests
from bs4 import BeautifulSoup

class Player(object):
	'''This class represents a Player in the NFL'''

	###############################################
	# Declare all static class variables here     #
	###############################################

	# Dictionary to hold names and rankings of defenses to compare to players data
	defenseRankings = {}

	# Store default data locations
	scheduleLoc = "current_week_schedule"

	# Store all of the links to gather data from
	statLink = "https://www.nfl.com/players/{0}/stats/"
	scheduleLink = "https://www.nfl.com/players/{0}/stats/logs/"
	defenseLink = "https://www.espn.com/nfl/stats/team/_/view/defense"
	gameLink = "https://www.espn.com/nfl/schedule"

	def __init__(self, name):

		# Holds all of the data relevant to the player
		self.name = name           # Holds the players name
		self.position = ""         # Holds the players position
		self.stats = []            # Holds all of the stats for the player for the past year
		self.gameStats = []        # Holds all of the stats per game for the current or past season
		self.gameCategories = []   # Holds all of the categories for the individual games
		self.schedule = []         # Holds the past schedule of the player
		self.opponent = ""         # Holds the current opponent
		self.score = 0             # Holds the final score value for the player
		self.categories = []       # Holds all of the data categories for the player

	def getData(self, dir):
		'''This method will make the HTTP request to the website in order to get the
		appropriate data. This data includes the players statistics going into the
		current week, as well as the teams that they have faced, and the team they
		are facing this week.'''

		# Create the link to the website
		link = Player.statLink.format(self.name)
		# Create the request to the webpage
		webpage = requests.get(link)
		# Make a temporary file to store the HTML
		file = open("{0}/{1}.html".format(dir, self.name), "w")
		# Save the webpage to the file
		file.write(webpage.text)
		file.close() # Close the file

		# Extract the data from the file
		with open("{0}/{1}.html".format(dir, self.name), 'r') as f:

			# Create a beautiful soup object to scrape through data
			soup = BeautifulSoup(f.read(), 'html.parser')

			# Get the players stats, their position, and column headers from the html
			position = soup.find_all('span', class_="nfl-c-player-header__position")

			# Get all of the total stats associated with the current or previous year

			stats = soup.find_all('tr')[-2].find_all('td')        # All of the accumulated stats for the past year
			categories = soup.find_all('thead')[1].find_all('th') # Categories of those stats for the past year
			self.position = position[0].text.strip()              # Store position of the player

			# Add team to the stats and cetegories first
			self.stats.append(stats[1].text.strip())
			self.categories.append("Team")

			for i in range(4, len(stats)):
				self.stats.append(stats[i].text.strip())
				self.categories.append(categories[i].text.strip())

			# Get all of the stats for each week of the season
			catList = [0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]  # represents the relevant columns of the stat table

			# gameTable consists of all of the games that have been played this season and the stats of the players for those games
			gameTable = soup.find_all('table')[0].find_all('tr')
			cats = gameTable[0].find_all('th')  # Categories for the stats stored for each individual game


			for i in catList: # Skips the result of the game that week, unimportant
				self.gameCategories.append(cats[i].text.strip())  # Append the stat categories to gameCategories list

			# Go through each week and gather the reevant data
			for i in range(1,len(gameTable)):
				tempArr = []  # Each week will be stored in an array of its own
				currentWeek = gameTable[i].find_all('td') # Get each week in the game table and store it here
				for i in catList:  # Only grab the relevant columns
					tempArr.append(currentWeek[i].text.strip())  # Append each stat to the temp array representing a game
				self.gameStats.append(tempArr)   # Append this weeks game to the gameStats

			# Sort the game stats
			self.sortGameStats() 

			# Used to find the data categories
			#temp = soup.find_all('thead')[0]
			#categories = temp.find_all('th')

			# Update the current players position
			#self.position = position[0].text.strip()
			# Go through all of the 2020 data
			#i = 1
			#current = stats[-(i)].text.strip()
			#print(current)
			# Go until all of the data is found and add it to the data array
			#while(current != '2020'):
			#	self.stats.append(current)
			#	i += 1
			#	current = stats[-(i)].text.strip()
			# Add the year manually
			#self.stats.append(current)

			# Go through all of the catefories and update the dataCategories attribute
			#for i in range(len(categories)):
			#	self.categories.append(categories[-(i+1)].text)

	def sortGameStats(self):
		'''This method will sort the game stats after they are gathered. This is necessary due to the fact that 
		NFL.com gives these stats out of order and they muist be in order for graphing to work. Implements bubble sort.'''


		sorted = False  # Initialize sorted to False

		# Go through the game stats list until it is osrted
		while(not sorted):
			# Start each iteration assuming list is sorted
			sorted = True 
			# Go through the list and swap adjacent values that are out of order
			for i in range(0, len(self.gameStats) - 1):
				val1 = int(self.gameStats[i][0])
				val2 = int(self.gameStats[i+1][0])

				if(val2 < val1): # Compare current position with the next position
					sorted = False  # If true list is not sorted and needs at least one more iteration
					# Swap the values
					temp = self.gameStats[i]
					self.gameStats[i] = self.gameStats[i+1]
					self.gameStats[i+1] = temp
				

	def getScheduleData(self, dir):
		'''This method will get the opponents defenses that the player has faced
		up until this point'''

		# Create the link to get the games played so far
		link = Player.scheduleLink.format(self.name)
		# Make the HTTP request and save it to the file
		webpage = requests.get(link) # Stores the opponents played against
		file = open("{0}/{1}.html".format(dir, self.name + "_schedule"), "w")
		# Save the webpage to the file
		file.write(webpage.text)
		file.close() # Close the file

		# Extract the defenses that have been played against
		with open("{0}/{1}.html".format(dir, self.name + "_schedule"), "r") as f:
			# Create a BeautifulSoup object to parse the data
			soup = BeautifulSoup(f.read(), 'html.parser')
			# Isolate all of the tr elements
			data = soup.tbody.find_all('tr')
			# Go through each table in the data and
			for table in data:
				# Grab all of the td elements in the table
				values = table.find_all('td')
				# Get the 3rd value in the list representing the team faced
				opp = values[2].text.strip()
				# Remove the first value of the String if it is an @ symbol
				if("@" in opp):
					opp = opp[1:]

				if(opp == 'Football Team'):
					opp = "Washington"
				# Append the value into the players schedule
				self.schedule.append(opp)


	def getOpponent(self, dic):
		'''This method will take in a dictionary holding all of this weeks
		games and then find the current players opponent of the week'''


		opp = "Bye Week"                    # Create a default value for opponent
		team = self.stats[0].split()[-1]    # Takes the team and separates the city
		print(team)

		# Account for Washington Football Team
		if (team == "Team"):
			team = "Washington"

		# Search through the dictionary
		for k, v in dic.items():
			if team in k:     # Team is away this week
				opp = v
			elif(team in v):  # Team is home this week
				opp = k

		# Update the opponent attribute of the player
		self.opponent = opp


	def calculateScore(self):
		'''This method will use all of the data collected for the current player
		along with the general data gathered for defenses to caluclate a score
		associated with the player, which represents their value in the current
		week of the season.'''

		# When the current player is on a bye, give them a zero and exit the function
		if(self.opponent == "Bye Week"):
			self.score = 0
			return

		# First get the average defense that this player has faced up until now
		avg_def = [0.0 ,0.0, 0.0, 0.0]
		cur_def = Player.defenseRankings[self.opponent] # Get this weeks opponent

		# Go through each of the defenses faced so far
		for team in self.schedule:
			# Get the defensive stats of current defense
			stats = Player.defenseRankings[team]
			# Add each of the stats to the average defense
			for i in range(len(stats)):
				avg_def[i] += float(stats[i])

		# Divide each statistic by the number of teams played
		for i in range(len(avg_def)):
			avg_def[i] /= len(self.schedule)

		# Get the difference between the average defense and the current one
		diff = [float(cur_def[i]) - avg_def[i] for i in range(4)]

		self.score = len(self.name)


	def printPlayer(self):
		'''This method Takes all of the available data for the current player
		and prints it to the console neatly.'''

		print(self.name + ", Position: " + self.position)
		#print("This Week's Opponent: {0}".format(self.opponent))
		#print("Fantasy Score: {0}".format(self.score))
		print("\nPLAYER DATA:\n")

		for i in range(len(self.stats)):
			print("\t" + self.categories[i] + " --> " + self.stats[i])

		print("\nTEAMS PLAYED: \n")
		for s in self.schedule:
			print("\t --> " + s)

####################################################
# STATIC METHODS
####################################################

	@staticmethod
	def printDefenseData():
		'''This static method will print the current data that is stored for
		the defenses as apart of all Player objects'''

		# Go through each of the defenses currently stored
		for k, v in Player.defenseRankings.items():
			# Print the team name first
			print(k + ":\n")
			print("   --> Total yds/g: {0} , Passing yds/g: {1} , Rushing yds/g: {2} , Points/g : {3}"
				.format(v[0], v[1], v[2], v[3]))
			print()


	@staticmethod
	def getDefenseRankings(dir):
		'''This method will go through ESPN data and get all passing and rushing
		stats for all defenses in the NFL. Results will be stored in the instance
		variable defenseRankings'''

		# Make the request to the webpage at ESPN
		webpage = requests.get(Player.defenseLink)
		# Create the file to store the resulting webpage
		file = open("{0}/{1}.html".format(dir, "espn_defenses"), "w")
		file.write(webpage.text)  # Write the HTML to file
		file.close()              # Close the file

		# Open the file and extract the data
		with open("{0}/{1}.html".format(dir, "espn_defenses"), "r") as f:
			# Create a BeautifulSoup object to parse the data
			soup = BeautifulSoup(f.read(), 'html.parser')
			# Get all of the tables that store the teams defense data
			tables = soup.find_all('tr', class_ = "Table__TR--sm")

			# Go through the tables and add name and data to the Player.defenseRankings
			for i in range(32):
				# Get the team name
				team_name = tables[i].text.split()[-1]
				# Get the correct data
				temp_list = []     # Used to store the relevant data
				# Get the data for the team as a list
				temp_data = tables[i+32].find_all('div')
				# Add correct data to the list
				temp_list.append(temp_data[2].text)
				temp_list.append(temp_data[4].text)
				temp_list.append(temp_data[6].text)
				temp_list.append(temp_data[8].text)
				# Add the list and the team name to the dictionary
				Player.defenseRankings[team_name] = temp_list

		# Add a entry for a bye week
		Player.defenseRankings["Bye Week"] = [0.0, 0.0, 0.0, 0.0]

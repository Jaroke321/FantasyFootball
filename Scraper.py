import os
import requests
import sys
from bs4 import BeautifulSoup
from Defense import Defense
from Player import Player


class Scraper(object):
    '''This class will be used to handle all of the data and file maintainence
    associated with scraping.'''

    ###########################################
    # Declare all static class varibales here #
    ###########################################

    # Used to get the current week that will be used for all Scraper objects
    gameLink = "https://www.espn.com/nfl/schedule"

    weekNumber = -1   # Used to store the current week number, default -1
    scraperCount = 0  # Used to count number of scrapers being used at once

    schedule = {}     # Stores all of the matchups for the week


    def __init__(self, file = None):

        # Initialize all of the variables associated with the scraper objects
        self.players = []          # Holds all of the players in the Fantasy team
        self.defense = []          # Holds all of the Defenses in the Fantasy team
        self.team = {}             # Holds the resulting team of players

        Scraper.scraperCount += 1  # Increment the count class variable
        # Used to name each team in case multiple scrap objects exist
        self.teamName = "Team #{0}".format(Scraper.scraperCount)
        # Create a temp directory to store data for each scraper object
        self.tempDir = "temp_{0}".format(Scraper.scraperCount)
        # Create the data directory that is associated with this Scraper
        self.makeDataDirectory()

        # Create data directory and update the current week when first Scraper is created
        if (Scraper.weekNumber == -1):
            # Get the current weeks schedule
            Scraper.getCurrentWeek(self.tempDir)

        # If the user entered a file then load it here
        if file:
            self.loadFile(file)


    def loadFile(self, filename):
        '''This method will load in all of the players from the players file'''

        # Check if the file exists
        file = os.path.join(os.getcwd(), filename)
        if(not os.path.isfile(file)):
            print("ERROR: The file you entered does not exit")
            sys.exit()

        # open players file and cycle through each line until the end
        with open(filename, 'r') as reader:
            for line in reader:
                # Check if the current line in the file is a player or a defense
                if(line[0:7] != "defense"):
                    # Create a new player and add them to the players list
                    newPlayer = Player(line.rstrip())
                    self.players.append(newPlayer)
                else:
                    # Create a new Defense and add them to the defense list
                    newDefense = Defense(line[9:].rstrip())
                    self.defense.append(newDefense)


    def getPlayerData(self):
        '''This method will use the previously loaded players to make get
        requests to NFL.com in order to retrieve the HTML'''

        # Get the current defense stats and upcoming schedule
        Player.getDefenseRankings(self.tempDir)

        # Go through each player
        for player in self.players:
            # Get data for players
            player.getData(self.tempDir)          # Gather all of the players stats
            player.getScheduleData(self.tempDir)  # Get the opponents faced so far
            player.getOpponent(Scraper.schedule)  # Get upcoming opponent
            player.calculateScore()               # Calculate the final Fantasy score


    def getDefenseData(self):
        '''This method will go through the list of available defenses and
        call the appropriate methods in order to get all of the data for
        each defense.'''

        # Get the general offense data
        Defense.getOffenseRankings(self.tempDir)

        # Cycle through each defense and get the data
        for d in self.defense:
            # Get the data for the defense
            d.getData(self.tempDir)           # Gets all of the general data
            d.getSchedule(self.tempDir)       # Gets all of the offenses already played
            d.calculateScore()                # Calculate the Fantasy score of the defense


    def getAllData(self):
        '''This method will gather all of the data for the players and
        the defenses at once. Alerting the user on the progress throughout.'''

        # Start the process by getting the players data
        print("Retrieving Players Data...")
        self.getPlayerData()
        print("Done")

        # Continue to get the defenses data
        print("Retrieving Defense data")
        self.getDefenseData()
        print("Done")

        # Delete all of the temporary files created
        print("Deleting all temporary files created")
        self.deleteDataDirectory()
        print("Done")

    def printTeam(self):
        '''This method will order the players and defenses in order to determine
        which are the best to start this week.'''

        print("\n\nFinalized Team:\n\n")
        print("Offensive PLayers:\n")

        # Go through the team attribute and print the players to console
        for k, v in self.team.items():
            print(k)
            for p in v:
                print("\t-" + p.name + " : " + str(p.score))

        print("\nDefensive Teams:\n")
        # Go through the defense and print the sorted defenses
        for d in self.defense:
            print("\t-" + d.team + " : " + str(d.score))

        print()


    def sort(self):
        '''This method is used to sort the players and defenses in order of their
        Fantasy points.'''

        # First organize all of the players by position
        players = {} # Create a dictionary to hold all of the players by position
    
        # Go through each player and add them to the dictionary
        for p in self.players:
            if p.position in players:
                players[p.position].append(p)
            else:
                players[p.position] = [p]

        # Sort each of the lists
        for k, v in players.items():

            sorted = False
            while(not sorted):
                sorted = True
                for i in range(len(v) - 1):
                    if(v[i].score < v[i+1].score):
                        temp = v[i+1]
                        v[i+1] = v[i]
                        v[i] = temp
                        sorted = False

        # Set the team attribute to this sorted dictionary
        self.team = players

        sorted = False
        # Sort the defenses
        while(not sorted):
            sorted = True
            for i in range(len(self.defense) - 1):
                if(self.defense[i] < self.defense[i + 1]):
                    temp = self.defense[i+1]
                    self.defense[i + 1] = self.defense[i]
                    self.defense[i] = temp
                    sorted = False


    def save(self, file):
        '''This method will save the current team to a file with the week number
        with the team ranked. If file is None, default file location will be used.'''

        loc = "Week_{0}.txt".format(Scraper.weekNumber) # Default save location
        # Check if the user entered a different save location
        if(file):
            loc = file

        # Open the file for writing
        with open(loc, "w") as f:
            # Start with a header
            f.write("Fantasy Team for week {0}".format(Scraper.weekNumber))
            # Write the players in by position
            f.write("\n\nPlayers:\n\n")
            # Cycle through each of the position and the players and write to file
            for k, v in self.team.items():
                f.write("{0}:\n".format(k))
                for p in v:
                    f.write("  - {0} , score = {1}\n".format(p.name, p.score))

            f.write("\nDefenses:\n")
            # Write in the Defenses
            for d in self.defense:
                f.write("  - {0} , score = {1}\n".format(d.team, d.score))


    @staticmethod
    def getCurrentWeek(dir):
        '''This method takes in a directory name and gathers both the current
        week number in the NFL and the current matchups this week.'''
        # Make the request to ESPN
        webpage = requests.get(Scraper.gameLink)
        # Create and open the file
        file = open("{0}/{1}.html".format(dir, Player.scheduleLoc), "w")
        file.write(webpage.text)  # Write the html to the file
        file.close()              # Close the file

        # Open the file and het the current week number
        with open("{0}/{1}.html".format(dir, Player.scheduleLoc), "r") as f:
            # Create a beautiful soup object
            soup = BeautifulSoup(f.read(), 'html.parser')
            # Get the dropdown menu that selects each weeks schedule
            dropdown = soup.find('div', class_="dropdown-type-week")
            # Extract from dropwdown the current week option
            weekOption = dropdown.find(selected="selected")
            # Update the class attribute that holds the current week
            Scraper.weekNumber = weekOption.text.split()[1]

            # Get all of the teams matchups for the week
            matchups = soup.find_all('a', class_="team-name")
            # Cycle through each game and get the away and home teams
            for i in range(0, len(matchups), 2):
                away = matchups[i].abbr.get('title').split()[-1]
                home = matchups[i+1].abbr.get('title').split()[-1]
                Scraper.schedule[away] = home


    def print(self):
        '''This method will list all of the players that are currently
        loaded into the players attribute'''

        for player in self.players:
            print("  --> " + player.name)

        print("\nDefenses to choose from:\n")

        for d in self.defense:
            print("  --> " + d.team)


    def makeDataDirectory(self):
        '''This method creates a temporary data directory to be used to
        store HTML files collected throughout the scraping process'''

        # Create the path for the directory in the current directory
        directory = self.tempDir
        current = os.getcwd()
        path = os.path.join(current, directory)

        # Try to make the directory, error if it already exists
        try:
            os.mkdir(path)
        except OSError as e:  # Directory already exists
            print("Data directory is already created")


    def deleteDataDirectory(self):
        '''This method deletes all of the temporary files in the data
        directory and then deletes the data directory. This method should
        be called at the end of the scraping process'''

        # Get the path of the data directory
        data = self.tempDir
        current = os.getcwd()
        path = os.path.join(current, data)
        # list all of the files within the directory
        files = os.listdir(path)

        # Cycle through the files and delete them
        for f in files:
            os.remove(os.path.join(path, f))

        # Remove the entire Directory
        os.rmdir(path)


    def printCurrentData(self):
        '''This method is used as a simple tool to check on the data at any
        point during operations.'''

        # Create spaces for the current team and print team name
        print("\n")
        print(self.teamName + "\n")

        # Go through each player object and call the print method
        for player in self.players:

            # Print the players
            player.printPlayer()
            print() # Create a space between players and Defense

        # Print the Defense
        for defense in self.defense:
            defense.printDefense()

    def printDefenseStats(self):
        '''This method simply prints the general defense stats that are
        stored within the Player object as a class variable.'''

        print("\nCurrent Defense Data:\n")
        Player.printDefenseData()

    def printOffenseStats(self):
        '''This method will print the class variable that is apart of the
        Defense class that stores all of the general Offense data.'''

        print("\nCurrent Offense Data:\n")
        Defense.printOffenseData()

    def printSchedule(self):
        '''This method will print the week number and the current scheudle in a
        neat and readable way to the console.'''

        print("\n*****************************************")
        print("*\t\tWeek#{0}\t\t\t*".format(Scraper.weekNumber))
        print("*****************************************")

        print("\nThis Week's NFL Schedule\n")
        for k, v in Scraper.schedule.items():
            print("  - " + k + " @ " + v)
            print()

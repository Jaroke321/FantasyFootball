import matplotlib.pyplot as plt 
import numpy as np 

class Grapher(object):
    '''Grapher object that is built to use NFL player data and defense data 
    in order to generate matplotlib graphs to the user.'''

    #########################################
    # STATIC VARIABLES
    #########################################

    # Team colors that will be used to distinguish between different players
    teamColor = {"Arizona Cardinals": "#97233F", "Baltimore Ravens": "#241773", "Carolina Panthers": "#0085CA",
                 "Cincinnati Bengals": "#FB4F14", "Dallas Cowboys": "#041E42", "Detroit Lions": "#0076B6",
                 "Houston Texans": "#03202F", "Jacksonville Jaguars": "#9F792C", "Los Angeles Chargers": "#002A5E",
                 "Miami Dolphins": "#008E97", "New England Patriots": "#B0B7BC", "New York Giants": "#0B2265", 
                 "Oakland Raiders": "#000000", "Pittsburgh Steelers": "#101920", "Seattle Seahawks": "#69BE28", 
                 "Tennessee Titans": "#4B92DB", "Atlanta Falcons": "#A71930", "Buffalo Bills": "#00338D",
                 "Chicago Bears": "#C83803", "Cleveland Browns": "#311D00", "Denver Broncos": "#FB4F14",
                 "Green Bay Packers": "#203731", "Indianapolis Colts": "#002C5F", "Kansas City Chiefs": "#E31837",
                 "Los Angeles Rams": "#003594", "Minnesota Vikings": "#4F2683", "New Orleans Saints": "#D3BC8D",
                 "New York Jets": "#125740", "Philadelpha Eagles": "#004C54", "San Francisco 49ers": "#AA0000",
                 "Tampa Bay Buccaneers": "#D50A0A", "Washington Football Team": "#773141"}


    def __init__(self, rankings, statList):
        '''Constructor function for the Grapher class. The ranking argument will take in the league offensive
         or defensive rankings depending if the grapher is using a defense or player for an object. The statList 
         argument is the list of players or defenses the user is attempting to graph.'''

        # Create object variables
        self.rankings = rankings
        self.statList = statList


    ###################################
    # Static methods
    ###################################

    @staticmethod
    def graphSinglePlayer(player, defenseRankings):
        '''This method will be used for the search player function in the Scraper class to display the 
        correct graphs for a single player'''

        mainColor = Grapher.teamColor[player.stats[0]] # Grabs the main color for the team the player is apart of

        # These lists represent the x and y vlues of the first plot
        statArray = []
        weeks = []
        
        # Populate the lists with each value of the x axis representing a week in the NFL
        for game in player.gameStats:
            weeks.append(int(game[0]))  # Week number
            # Passing yards for wach week in the y axis
            if(not (game[4] == '')):     
                statArray.append(int(game[4]))
            else:
                statArray.append(0)

        y1 = np.array(statArray)
        x1 = np.array(weeks)

        plt.plot(x1, y1, c = mainColor)

        plt.grid(linestyle = '--', linewidth = 0.5)

        plt.xlabel("Week")
        plt.ylabel("Passing Yards")

        plt.title("Passing Yards / Week VS. Defenses")

        plt.suptitle(str(player.name))

        plt.show()  # Print the final graph for the player

    @staticmethod
    def graphSingleDefense(defense):
        '''This method will be used for the search defense function in the scraper class to display the 
        correct graphs for a single player.'''



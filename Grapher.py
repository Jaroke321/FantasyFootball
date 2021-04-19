import matplotlib.pyplot as plt 
import numpy as np 

class Grapher(object):
    '''Grapher object that is built to use NFL player data and defense data 
    in order to generate matplotlib graphs to the user.'''

    #########################################
    # STATIC VARIABLES
    #########################################

    # Team colors that will be used to distinguish between different players
    teamColor = {"Arizona Cardinals": ["#97233F", "#000000"], "Baltimore Ravens": ["#241773", "#9E7C0C"], 
                 "Carolina Panthers": ["#0085CA", "#101820"], "Cincinnati Bengals": ["#FB4F14", "#000000"], 
                 "Dallas Cowboys": ["#041E42", "#869397"], "Detroit Lions": ["#0076B6", "#B0B7BC"],
                 "Houston Texans": ["#03202F", "#A71930"], "Jacksonville Jaguars": ["#006778", "#9F792C"], 
                 "Los Angeles Chargers": ["#002A5E", "#FFC20E"], "Miami Dolphins": ["#008E97", "#FC4C02"], 
                 "New England Patriots": ["#002244", "#C60C30"], "New York Giants": ["#0B2265", "#A71930"], 
                 "Oakland Raiders": ["#000000", "#A5ACAF"], "Pittsburgh Steelers": ["#101920", "#FFB612"], 
                 "Seattle Seahawks": ["#002244", "#69BE28"], "Tennessee Titans": ["#0C2340", "#4B92DB"], 
                 "Atlanta Falcons": ["#A71930", "#000000"], "Buffalo Bills": ["#C60C30", "#00338D"],
                 "Chicago Bears": ["#0B162A", "#C83803"], "Cleveland Browns": ["#311D00", "#FF3C00"], 
                 "Denver Broncos": ["#FB4F14", "#002244"], "Green Bay Packers": ["#203731", "#FFB612"], 
                 "Indianapolis Colts": ["#002C5F", "#A2AAAD"], "Kansas City Chiefs": ["#E31837", "#FFB81C"], 
                 "Los Angeles Rams": ["#003594", "#FFA300"], "Minnesota Vikings": ["#4F2683", "#FFC62F"], 
                 "New Orleans Saints": ["#D3BC8D", "#101820"], "New York Jets": ["#125740", "#000000"], 
                 "Philadelpha Eagles": ["#004C54", "#A5ACAF"], "San Francisco 49ers": ["#AA0000", "#B3995D"], 
                 "Tampa Bay Buccaneers": ["#D50A0A", "#34302B"], "Washington Football Team": ["#773141", "#FFB612"]}


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

        colors = Grapher.teamColor[player.stats[0]] # Grabs the main color and accet collor of the players team from the grapher
        mainColor = colors[0]        # Grabs the main color 
        accentColor = colors[1]      # Grabs the accent color
        plt.figure(figsize=(15,10))  # Sets the size of the graph when it is displayed

        # Create the fonts for the different component of the graphs
        font1 = {'family': 'serif', 'size': 15}
        title_font = {'family': 'serif', 'size': 20}

        # Generate the numpy arrays for the first plot
        graph1_x, graph1_y1, graph1_y2 = Grapher.graphArrayOne(player, defenseRankings)
        # Second plot arrays
        graph2_x, graph2_y = Grapher.graphArrayTwo(player, defenseRankings)
        # Third plot arrays
        graph3_x, graph3_y = Grapher.graphArrayThree(player, defenseRankings)
        # Fourth plot arrays
        graph4_x, graph4_y = Grapher.graphArrayFour(player, defenseRankings)

        # Plot 1
        plt.subplot(2, 2, 1)
        plt.plot(graph1_x, graph1_y1, marker = 'o', ms = 12, mec = accentColor, c = mainColor)
        plt.plot(graph1_x, graph1_y2, marker = 'o', ms = 8, c = "#000000")
        plt.grid(linestyle = '--', linewidth = 0.5)

        plt.xlabel("Week", fontdict = font1)
        plt.ylabel("Yards", fontdict = font1)
        plt.title("Yards / Week VS. Defenses")

        # Plot 2
        plt.subplot(2, 2, 2)
        plt.plot(graph2_x, graph2_y)
        plt.xlabel("label for graph 2", fontdict = font1)
        plt.ylabel("Label for graph 2", fontdict = font1)
        plt.title("Graph #2")

        # Plot 3
        plt.subplot(2, 2, 3)
        plt.plot(graph3_x, graph3_y)
        plt.xlabel("label for graph 3", fontdict = font1)
        plt.ylabel("Label for graph 3", fontdict = font1)
        plt.title("Graph #3")

        # Plot 4
        plt.subplot(2, 2, 4)
        plt.plot(graph4_x, graph4_y)
        plt.xlabel("label for graph 4", fontdict = font1)
        plt.ylabel("Label for graph 4", fontdict = font1)
        plt.title("Graph #4")

        # Add a supertitle to the whole window
        plt.suptitle(str(player.name), fontdict = title_font)

        plt.show()  # Print the final graph for the player

    @staticmethod
    def graphSingleDefense(defense):
        '''This method will be used for the search defense function in the scraper class to display the 
        correct graphs for a single player.'''


    @staticmethod
    def graphArrayOne(player, defenseRankings):
        '''This method is used by the graphSinglePlayer method to generate the arrays for the first plot'''

        yards_idx = player.gameCategories.index("YDS")  # Get the index of the yards column
        # Used to get the correct defense stat to compare the player to
        def_idx = 1
        if player.position == "RB" : def_idx = 2

        # Lists for the plots
        statArray = []    # Used in the first plot to represent the players stats
        weeks = []        # Used in the first plot to represent each week of football
        defense_arr = []  # Used in the first plot to represent the defenses the player faced
        
        # Populate the lists with each value of the x axis representing a week in the NFL
        for game in player.gameStats:
            weeks.append(int(game[0]))  # Week number
            defense_arr.append(float(defenseRankings[game[1]][def_idx]))  # Either pass defense or rush defense depending on position of player
            # Passing yards for wach week in the y axis
            if(not (game[yards_idx] == '')):     
                statArray.append(int(game[yards_idx]))
            else:
                statArray.append(0)

        return weeks, statArray, defense_arr
       

    @staticmethod
    def graphArrayTwo(player, defenseRankings):
        '''This method is used by the graphSinglePlayer method to generate the arrays for the second plot'''

        return [], []

    @staticmethod
    def graphArrayThree(player, defenseRankings):
        '''This method is used by the graphSinglePLayer method to generate the array for the third plot'''

        return [], []

    @staticmethod
    def graphArrayFour(player, defenseRankings):
        '''This method is used by the graphSinglePlayer method to generate the arrays for the fourth plot'''

        return [], []


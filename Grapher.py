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

        colors = Grapher.teamColor[player.stats[0][1]] # Grabs the main color and accet collor of the players team from the grapher
        mainColor = colors[0]           # Grabs the main color 
        accentColor = colors[1]         # Grabs the accent color
        plt.figure(figsize = (18, 12))  # Sets the size of the graph when it is displayed

        # Create the fonts for the different component of the graphs
        font1 = {'family': 'serif', 'size': 15}
        title_font = {'family': 'serif', 'size': 20}

        # Generate the numpy arrays for the first plot
        graph1_x, graph1_y1, graph1_y2 = Grapher.playerArrayOne(player, defenseRankings)
        # Second plot arrays
        graph2_x, graph2_y, graph2_lbl = Grapher.playerArrayTwo(player, defenseRankings)
        # Third plot arrays
        graph3_x, graph3_y = Grapher.playerArrayThree(player, defenseRankings)
        # Fourth plot arrays
        graph4_x, graph4_y = Grapher.playerArrayFour(player, defenseRankings)

        # Plot 1
        plt.subplot(2, 2, 1)
        plt.plot(graph1_x, graph1_y1, marker = 'o', ms = 12, mec = accentColor, c = mainColor)
        plt.plot(graph1_x, graph1_y2, marker = 'o', ms = 8, c = "#000000")
        plt.grid(linestyle = '--', linewidth = 0.5)

        plt.xlabel("Week", fontdict = font1)
        plt.ylabel("Yards", fontdict = font1)
        plt.title("Yards VS. Defenses")

        # Plot 2
        plt.subplot(2, 2, 2)
        barwidth = 0.25   # Width of the bars in the graph
        bar_list = []     # Will hold the x positions of all of the bars

        # Populate the bar list using the list of y values we have
        bar_list.append(np.arange(len(graph2_y[0])))
        color_list = [[mainColor, mainColor],[accentColor, accentColor],["#FFFFFF", mainColor]]

        # Determine the location of the bars
        for i in range(len(graph2_y[1:])):
            bar_list.append([x + barwidth for x in bar_list[i]])

        # Make the plot using those bar_list values as the xs and the ys
        for i in range(len(graph2_y)):
            plt.bar(bar_list[i], graph2_y[i], color = color_list[i][0], width = barwidth, 
                    edgecolor = color_list[i][1], label = graph2_lbl[i])

        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("Year", fontdict = font1)
        plt.ylabel("Stats", fontdict = font1)
        plt.xticks([r + barwidth for r in range(len(graph2_y[0]))], graph2_x)
        plt.title("Stats Per Year")
        plt.legend()

        # Plot 3
        plt.subplot(2, 2, 3)
        plt.bar(graph3_x, graph3_y, color = mainColor, edgecolor = accentColor, label = "Yards")
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("Year", fontdict = font1)
        plt.ylabel("Yards", fontdict = font1)
        plt.xticks(graph3_x)
        plt.title("Yards Per year")
        plt.legend()

        # Plot 4
        plt.subplot(2, 2, 4)
        plt.plot(graph4_x, graph4_y)

        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("label for graph 4", fontdict = font1)
        plt.ylabel("Label for graph 4", fontdict = font1)
        plt.title("Graph #4")

        # Add a supertitle to the whole window
        plt.suptitle(str(player.name), fontdict = title_font)

        plt.show()  # Print the final graph for the player

    @staticmethod
    def graphSingleDefense(defense, offenseRankings):
        '''This method will be used for the search defense function in the scraper class to display the 
        correct graphs for a single player.'''

        # Get the appropriate main color and accent color from the color dictionary
        colors = Grapher.teamColor[]
        mainColor = colors[0]
        accentColor = colors[1]

        plt.figure(figsize = (18, 12)) # Sets the size of the window holding all four graphs

        # Create the fonts for the different component of the graphs
        font1 = {'family': 'serif', 'size': 15}
        title_font = {'family': 'serif', 'size': 20}

        # Get all of the arrays for the graphs
        graph1_x, graph1_y = Grapher.defenseArrayOne(defense, offenseRankings)
        graph2_x, graph2_y = Grapher.defenseArrayTwo(defense, offenseRankings)
        graph3_x, graph3_y = Grapher.defenseArrayThree(defense, offenseRankings)
        graph4_x, graph4_y = Grapher.defenseArrayFour(defense, offenseRankings)

        # Plot 1
        plt.subplot(2, 2, 1)
        plt.plot(graph1_x, graph1_y)

        # Set labels for graph 1
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("Label for graph #1", fontdict = font1)
        plt.ylabel("Label for graph #1", fontdict = font1)
        plt.title("Graph #1")

        # Plot 2
        plt.subplot(2, 2, 2)
        plt.plot(graph2_x, graph2_y)

        # Set the labels for graph 2
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("Label for graph #2", fontdict = font1)
        plt.ylabel("Label for graph #2", fontdict = font1)
        plt.title("Graph #2")

        # Plot 3
        plt.subplot(2, 2, 3)
        plt.plot(graph3_x, graph3_y)

        # Set the labels for graph 3
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("Label for graph #3", fontdict = font1)
        plt.ylabel("Label for graph #3", fontdict = font1)
        plt.title("Graph #3")

        # Plot 4
        plt.subplot(2, 2, 4)
        plt.plot(graph4_x, graph4_y)

        # Set the labels for graph 4
        plt.grid(linestyle = '--', linewidth = 0.5)
        plt.xlabel("Label for graph #4", fontdict = font1)
        plt.ylabel("Label for graph #4", fontdict = font1)
        plt.title("Graph #4")

        # Set the window title 
        plt.suptitle(str(defense.tean))
        # Display the graph
        plt.show()

    
    ##################################
    #  Array functions for players   #
    ##################################

    @staticmethod
    def playerArrayOne(player, defenseRankings):
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
            # Passing yards for each week in the y axis
            if(not (game[yards_idx] == '')):     
                statArray.append(int(game[yards_idx]))
            else:
                statArray.append(0)
        # Return the correct arrays
        return weeks, statArray, defense_arr
       

    @staticmethod
    def playerArrayTwo(player, defenseRankings):
        '''This method is used by the graphSinglePlayer method to generate the arrays for the second plot'''

        year_arr = []    # Used to holf the years that the player has played in NFL
        stat_arr = []    # Used to hold the relevant stats for the player per year
        label_arr = []   # Will the store the stat labels for the different columns
        cat_arr = [8, 9, 12]  # The columns with the data to show

        # Change the cat arr based on the position of the player
        if player.position == "RB":
            cat_arr = [6, 7]
        elif player.position == "WR":
            cat_arr = [4, 6, 8]

        
        # Go through each year the player has played
        for year in player.stats:
            year_arr.append(year[0])

        # Get each stat in their own list and append to the stat array
        for col in cat_arr:
            temp_list = []
            label_arr.append(player.categories[col])
            # Get each stat for each year the player has played
            for year in player.stats:
                temp_list.append(float(year[col]))
            stat_arr.append(temp_list)

        return year_arr, stat_arr, label_arr

    @staticmethod
    def playerArrayThree(player, defenseRankings):
        '''This method is used by the graphSinglePLayer method to generate the array for the third plot'''

        year_arr = []   # Used to hold the years the player has been in the league
        yards_arr = []  # Used to hold the yards for each year
        yrd_idx = 6     # Holds the index for the yards column in the players stats
        
        # Change the yard index depending on the players position
        if player.position != "QB":
            yrd_idx = 5

        # Go through each of the years in the players stats
        for year in player.stats:
            # Append the correct year and yards for that year into thir arrays
            year_arr.append(year[0])
            yards_arr.append(float(year[yrd_idx]))

        # Return both arrays, x then y
        return year_arr, yards_arr

    @staticmethod
    def playerArrayFour(player, defenseRankings):
        '''This method is used by the graphSinglePlayer method to generate the arrays for the fourth plot'''

        return [], []


    ####################################
    #   Array functions for defenses   #
    ####################################
    
    @staticmethod
    def defenseArrayOne(defense, offenseRankings):
        '''This method will be used by the graphSingledefense method to generate the arrays for the first plot'''

        return []. []

    
    @staticmethod
    def defenseArrayTwo(defense, offenseRankings):
        '''This method will generate the second graph arrays for the graphSingleDefense method'''

        return [], []

    @staticmethod
    def defenseArrayThree(defense, offenseRankings):
        '''This method will generate the arrays for the third plot in the graphSingleDefense method.'''

        return [], []

    
    @staticmethod
    def defenseArrayFour(defense, offenseRankings)
        '''This method will generate the arrays for the fourth plot in the graphSingleDefense method.'''

        return [], []

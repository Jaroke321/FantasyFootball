from Scraper import Scraper
import sys
import os
import getopt

def main():

    # Default variable values
    filename = 'players.txt' # Default filename
    verbosity = 1            # Default vebosity level for the program
    save = False             # Boolean to store whether or not to save outout to file
    outputfile = None        # Default value for the output file to save to

    # Use getopt to parse the arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'f:v:so:h',
            ["filename=", "verbosity=", "save", "outputfile=", "help", "sp=", "sd="])
    except getopt.GetoptError as err:
        print(err) # Print the error
        usage()    # Call usage to show user how app is used
        sys.exit() # Exit the program

    # Go through each of the arguments
    for o, a in opts:
        if o in ["-f", "--filename"]:
            filename = a
        elif(o in ["-v", "--verbosity"]):
            if int(a) in [1, 2, 3]:
                verbosity = int(a)
            else:
                print("ERROR: option -v requires a number between 1 and 3")
                sys.exit()
        elif(o in ["-s", "--save"]):
            # Save the output to the standard file
            save = True
        elif(o in ["-o", "--outputfile"]):
            # Save to the specified output file
            save = True
            outputfile = a
        elif o == "--sp":
            # User is searching for a player
            Scraper.searchPlayer(a)
            sys.exit()
        elif o == "--sd":
            # User is searching for a defense
            Scraper.searchDefense(a)
            sys.exit()
        elif(o in ["-h", "--help"]):
            usage()
            sys.exit()

    # Create the scraper object using the filename
    scraper = Scraper(file = filename)

    # Call the correct function to start the program
    if verbosity == 1:
        verbosity_one(scraper)
    elif verbosity == 2:
        verbosity_two(scraper)
    else:
        verbosity_three(scraper)

    # Check if the user wants to save to file
    if save:
        scraper.save(outputfile)


def verbosity_one(scraper):
    '''This method will call all of the appropriate functions from the Scraper
    object. This represents the minimum amount of verbosity from the program,
    meaning output to console will be minimal.'''

    print("verbosity of 1 is being used...")
    scraper.getAllData()
    scraper.sort()
    scraper.printTeam()


def verbosity_two(scraper):
    '''This method will use a Scraper object and call the appropriate methods
    while also giving the user some information about what is going on. This function
    represents the median verbosity.'''

    print("verbosity of 2 is being used\n")
    print("List of Players and Defenses found:")
    scraper.print()
    print("Gathering Player data...")
    scraper.getPlayerData()
    print("Done")
    print("Gathering Defense Data")
    scraper.getDefenseData()
    print("Done")
    print("Deleting the temporary data directory")
    Scraper.deleteDataDirectory(scraper.tempDir)
    print("Done\n\n")
    scraper.printSchedule()
    scraper.sort()
    scraper.printTeam()


def verbosity_three(scraper):
    '''This function will use a Scraper object and call the appropriate methods
    while also giving the user the most amount of information. This function will
    provide the most amount of information possible.'''

    print("verbosity of 3 is being used...")
    print("List of Players and Defenses found:")
    scraper.print()
    print("Gathering Player data...")
    scraper.getPlayerData()
    print("Done")
    print("Gathering Defense Data...")
    scraper.getDefenseData()
    print("Done")
    print("Deleting the Temporary data directory used...")
    Scraper.deleteDataDirectory(scraper.tempDir)
    print("Done\n\n")
    scraper.printSchedule()
    scraper.printCurrentData()
    print("\n\nAll of the general data gathered on offenses and defenses:\n\n")
    scraper.printOffenseStats()
    scraper.printDefenseStats()
    scraper.sort()
    scraper.printTeam()


def usage():
    '''This function will display the general information for FantasyFootball.py
    Including how to use it and the different flags available to the user when
    launching the application.'''

    print("\nAll of the Flags available to use:\n\n")

    print("   -f, --filename [filename]\t-> Allows the user to provide a filename to the program where " +
                            "the players names and defense are stored in a text file." +
                            " If a filename is not provided the default name of 'players.txt'" +
                            " will be used\n\n")

    print("   -v, --verbosity [level]\t-> Allows the user to define a level of verbosity that the" +
                            " program will have. Verbosity level can be 1, 2, or 3." +
                            " Default verbosity is set to 1 if a value is not specified\n\n")

    print("   -s, --save\t\t\t-> This flag will allow the user to have the output of the" +
                            " program be saved to a file in the working directory." +
                            " No value is needed when using this flag. By default the" +
                            " program will not save the output to a file.\n\n") 

    print("   -o, --outputfile [filename]\t-> Allows you to define the output file you would want to use " + 
                            "to save the data to.")

    print("   -h, --help\t\t\t-> Displays the help screen describing all of the available flags.")


if __name__ == '__main__':
    main()

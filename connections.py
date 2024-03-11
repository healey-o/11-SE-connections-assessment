from random import choice
from random import randint
import math

#connections.py is a simple terminal-based version of NY Times game Connections
#Created by Oliver Healey

#TEMPORARY - list of possible categories (will be changed to a database/text file/library later)
ALL_CATEGORIES = {
    "Low Volume": ["Whisper", "Murmur", "Mumble", "Hush"],
    "Physics Terms": ["Velocity", "Speed", "Momentum", "Acceleration"],
    "Calmness": ["Serenity", "Tranquility", "Harmony", "Peace"],
    "Gemstones": ["Sapphire", "Emerald", "Ruby", "Topaz"],
    "Brightness": ["Illuminate", "Radiate", "Gleam", "Shine"],
    "Thinking Deeply": ["Ponder", "Contemplate", "Reflect", "Meditate"],
    "Music Elements": ["Melody", "Bass", "Rhythm", "Tune"],
    "Speed": ["Brisk", "Swift", "Rapid", "Quick"],
    "Shades of Blue": ["Azure", "Cerulean", "Cobalt", "Indigo"],
    "Powerful Winds": ["Whirlwind", "Cyclone", "Tornado", "Hurricane"]
    }

#Selects four random categories of words
def GetRandomCategories():
    categories = {}

    while len(categories) < 4:#Picks 4 random categories
        randomChoice = choice(list(ALL_CATEGORIES.keys()))
        
        if randomChoice not in list(categories.keys()):
            categories[randomChoice] = ALL_CATEGORIES[randomChoice]

    return categories

#Combines all words in the given categories into a single list
def WordListFromGrid(grid:list):
    words = []

    for row in grid:
        for word in row:
            words.append(word)
    
    return words

#Takes the four categories and randomly places their words in a 4x4 grid
def RandomizeGrid(categories:dict):
    
    randomGrid = []

    gridWords = []

    for category in categories:
        for word in categories[category]:
            gridWords.append(word)
    
    
    #Places these words in random positions in the list
    for y in range(4):
        row = []

        for x in range(4):
            selectedWord = gridWords.pop(randint(0,len(gridWords)-1)) #popping ensures each word is used once
            row.append(selectedWord)
        
        randomGrid.append(row)
    
    return randomGrid

#Displays the grid and associated info to the player
def DisplayGrid(grid, foundCategories):
    global lives

    print("\nCreate four groups of four!")

    gridWords = WordListFromGrid(grid)

    #Each grid 'tile' is the width of the longest word, plus a border of 3 spaces each side
    tileWidth = len(max(gridWords, key=len)) + 6

    #Internal function - adds lines around each row of categories
    def draw_line():
        for i in range((tileWidth+2)*4):#Add line between each row of categories
            print("-",end="")

    for row in grid:
        
        if grid.index(row) <= (len(foundCategories) - 1): #When the line is displaying guessed categories, change text colour
            print("\u001b[32m")
        else:
            print("\u001b[37m")

        draw_line()
        print("\n")
        
        for word in row:
            print("|",end="")

            print(word.center(tileWidth),end="") #Centres each word in the same sized box

            print("|",end="")
        
        print("\n")

        draw_line()

        

    print("\nMistakes remaining:", end="")#Lives counter
    for i in range(lives):
        print(" •",end="")
    print("\n")

#Edits the grid with any successfully guessed categories at the top
def RedrawGrid(foundCategories, grid):
    newGrid = []

    gridWords = WordListFromGrid(grid)

    if len(foundCategories) > 0: #Adds found categories to the top of the new grid
        for foundCategory in foundCategories:
            newGrid.append(foundCategories[foundCategory])
            
            for word in foundCategories[foundCategory]: #Removes the found category words from grid_words
                gridWords.pop(gridWords.index(word))

        for y in range(4-len(foundCategories)): #Adds the remaining words to the grid
            row = []

            for x in range(4):
                selectedWord = gridWords.pop(0) #Adds words that have not been guessed correctly back to the grid in the same order as before
                row.append(selectedWord)
            
            newGrid.append(row)
    else:
        newGrid = grid

    return newGrid

#Prompts the player for their four guesses
def GetGuesses():
    global lives

    guesses = []
    gridWords = WordListFromGrid(grid)

    while len(guesses) < 4:
        #All guesses are be made lowercase for easier matching
        guess = input("Enter a word from the grid:").lower()
        
        valid = False

        for word in gridWords:
            if guess == word.lower() and guess not in guesses:
                guesses.append(guess)
                valid = True

        if not valid:
            print("Sorry, that response is not valid. Please try again.")

        
    return guesses

#Checks the player's guesses against the four categories
def CheckGuesses(guesses, categories, foundCategories):
    global lives

    correct_count = 0 # counts number of correct words for each category

    for category in categories:
        if correct_count < 4: #Loops through each category until a match is found or there are no more categories

            correct_count = 0

            for word in categories[category]:
                if (word.lower() in guesses):
                    correct_count += 1
            
            if correct_count == 4:
                foundCategories[category] = categories[category]
                print(f"Correct! Found Category: {category}")
            elif correct_count == 3:
                print(f"One away...")
    
    if correct_count < 4: #If no category matches, lose a life
        lives -= 1
        print(f"Sorry, that is not correct.") 


    return foundCategories

#Checks if all categories have been found
def CheckWin(foundCategories):

    if len(foundCategories) == 4:
        return True
    else:
        return False

#Asks the player if they wish to play again or exit
def PromptPlayAgain():
    
    playAgain = input("Do you want to play again? (Y/N)")

    if playAgain.lower() in ["y","yes"]:
        return True
    elif playAgain.lower() in ["n", "no", "get me out of here"]:
        return False
    else:
        print("Please enter Y or N.")
        return PromptPlayAgain()
    

#Main game loop - Displays the grid then prompts for and checks guesses
def GameLoop(categories, grid, foundCategories):

    DisplayGrid(grid, foundCategories)

    guesses = GetGuesses()
    foundCategories = CheckGuesses(guesses, categories, foundCategories)


#Main script - initializes the variables, then runs the main game loop until the game ends.

if __name__ == "__main__":
    playing = True

    while playing:
        categories = GetRandomCategories()
        foundCategories = {}

        grid = RandomizeGrid(categories)

        lives = 4 #Lives is used as a global variable as its value is often changed within functions

        gameWon = False

        #Runs the game loop for the duration of the game
        while lives > 0 and not gameWon:
            GameLoop(categories, grid, foundCategories)

            grid = RedrawGrid(foundCategories, grid) #Updates the grid variable after each loop

            gameWon = CheckWin(foundCategories) #Checks if the game is completed
        
        if gameWon:
            if lives == 1:
                print("Phew!")
            print("Congratulations! You win!")
        else:
            print("Sorry, you have run out of lives.")
        
        playing = PromptPlayAgain()
    



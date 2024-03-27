from random import randint
import sqlite3
from time import sleep
import string

#connections.py is a simple terminal-based version of NY Times game Connections
#Created by Oliver Healey

#Selects four random categories of words from the database
def GetRandomCategories():
    #Connect to database
    categoriesConnection = sqlite3.connect('categories.db')
    cursor = categoriesConnection.cursor()

    cursor.execute("SELECT * FROM categories ORDER BY RANDOM() LIMIT 4") #Selects 4 random rows of the database
    #The first option in each row of the database is the category name, and the remaining 4 are the words in said category

    categories = {}

    for category in cursor.fetchall():
        categories[category[0]] = [category[1],category[2],category[3],category[4]]

    categoriesConnection.close()

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
def DisplayGrid(grid, foundCategories, gameWon):
    global lives

    if not gameWon:
        print("\n\u001b[33mCreate four groups of four!")

    gridWords = WordListFromGrid(grid)

    #Each grid 'tile' is the width of the longest word, plus a border of 3 spaces each side
    tileWidth = len(max(gridWords, key=len)) + 6

    #Internal function - adds lines around each row of categories
    def draw_line():
        for i in range((tileWidth+2)*4):#Add line between each row of categories
            print("-",end="")

    for row in grid:
        if grid.index(row) <= (len(foundCategories) - 1): #When the line is displaying guessed categories, change text colour and print the category name
            print("\u001b[32m")
            print(f"Category: {list(foundCategories.keys())[grid.index(row)]}")
        else:
            print("\u001b[37m")

        draw_line()
        print("\n")
        
        for word in row:
            print("|",end="")

            print(word.upper().center(tileWidth),end="") #Centres each word in the same sized box

            print("|",end="")
        
        print("\n")
        draw_line()

    print("\n\u001b[31mMistakes remaining:", end="")#Lives counter
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
def GetGuesses(foundCategories):
    global lives

    validGuesses = []
    gridWords = WordListFromGrid(grid)

    guess = input("\u001b[33mEnter a word from the grid, or enter 4 words:\u001b[37m ").lower() #This input runs before the others to check if the player is entering several words

    if " " in guess and len(guess.split()) == 4: #Allows all 4 guesses at once
        guesses = guess.split()

        for guessSplit in guesses:#Check if each word is valid
            valid = False

            guessSplit = guessSplit.translate(str.maketrans('', '', string.whitespace)) #Removes spaces

            alreadyFound = False

            for category in foundCategories: #Check that the word is not a part of a category that has already been found.
                if guessSplit in [x.lower() for x in foundCategories[category]]:
                    alreadyFound = True

            if guessSplit in [x.lower() for x in gridWords] and guessSplit not in validGuesses and not alreadyFound:
                validGuesses.append(guessSplit)
                valid = True

            if not valid:
                print("\u001b[31mSorry, that response is not valid. Please try again.")
                return GetGuesses(foundCategories) #RECURSION WOOO
              
    else:
        i = 0
        while len(validGuesses) < 4:
            #All guesses are be made lowercase for easier matching
            if i > 0: #only runs after the first guess
                guess = input("\u001b[33mEnter a word from the grid:\u001b[37m ").lower()
            
            valid = False

            alreadyFound = False

            for category in foundCategories: #Check that the word is not a part of a category that has already been found.
                if guess in [x.lower() for x in foundCategories[category]]:
                    alreadyFound = True

            if not alreadyFound:
                for word in gridWords:
                    
                    if guess == word.lower() and guess not in validGuesses:
                        validGuesses.append(guess)
                        valid = True

            if not valid:
                print("\u001b[31mSorry, that response is not valid. Please try again.")
                if len(validGuesses) == 0:#Only full restarts the guesses if it is the first guess
                    return GetGuesses(foundCategories)
            
            print(f"\u001b[32mWords guessed: {", ".join(validGuesses)}")
            
            i+=1

    return validGuesses

#Checks the player's guesses against the four categories
def CheckGuesses(guesses, categories, foundCategories):
    global lives

    correctCount = 0 # counts number of correct words for each category

    for category in categories:
        if correctCount < 4: #Loops through each category until a match is found or there are no more categories

            for word in categories[category]: #Counts the number of correct guesses
                if (word.lower() in guesses):
                    correctCount += 1
            
            if correctCount == 4:
                foundCategories[category] = categories[category]
                print(f"\u001b[32mCorrect! Found Category: {category}")
            elif correctCount == 3: #Recognises when the guess is one away from correct
                print(f"\u001b[33mOne away...")
            
            if correctCount <= 3:
                correctCount = 0

    if correctCount < 4: #If no category matches, lose a life
        lives -= 1
        print(f"\u001b[31mThat is not correct.") 

    return foundCategories

#Checks if all categories have been found
def CheckWin(foundCategories):
    if len(foundCategories) == 4:
        return True
    else:
        return False

#Asks the player if they wish to play again or exit
def PromptPlayAgain():
    playAgain = input("\u001b[37mDo you want to play again? (Y/N)")

    if playAgain.lower() in ["y","yes"]:
        return True
    elif playAgain.lower() in ["n", "no", "get me out of here"]:
        return False
    else:
        print("\u001b[31mPlease enter Y or N.")
        return PromptPlayAgain() #MORE RECURSION


#Main game loop - Displays the grid then prompts for and checks guesses
def GameLoop(categories, grid, foundCategories):
    DisplayGrid(grid, foundCategories, False)

    guesses = GetGuesses(foundCategories)
    foundCategories = CheckGuesses(guesses, categories, foundCategories)


#Main script - initializes the variables, then runs the main game loop until the game ends.
if __name__ == "__main__":
    playing = True

    firstGame = True #Used to determine if a tutorial should be displayed - only true during frist play, not repeats

    while playing:
        categories = GetRandomCategories()
        foundCategories = {}

        grid = RandomizeGrid(categories)

        lives = 4 #Lives is used as a global variable as its value is often changed within functions

        gameWon = False

        #Intro
        print("\u001b[01mWelcome")
        sleep(1)
        print("To\u001b[00m")
        sleep(1)

        #Big Logo
        print("""
\u001b[36m
██████╗ ██╗   ██╗ ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
██████╔╝ ╚████╔╝ ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
██╔═══╝   ╚██╔╝  ██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
██║        ██║   ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
╚═╝        ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
\u001b[37m
""")
        sleep(2)

        if firstGame:
            print("\u001b[31mHow to Play: \u001b[32mIdentify categories in the grid, then type your guess. You can either enter words one at a time, or all together and separated by spaces.")

            input("Press \u001b[34m[Enter]\u001b[32m to begin.\u001b[37m")

        #Runs the game loop for the duration of the game
        while lives > 0 and not gameWon:
            GameLoop(categories, grid, foundCategories)

            grid = RedrawGrid(foundCategories, grid) #Updates the grid variable after each loop

            gameWon = CheckWin(foundCategories) #Checks if the game is completed
        
        if gameWon:
            DisplayGrid(grid, foundCategories, gameWon)

            if lives == 1:
                print("Phew!")
            print("\u001b[32mCongratulations! You win!")
        else:
            print("\u001b[31mSorry, you have run out of lives.")
        
        playing = PromptPlayAgain()
        
        if firstGame:#Prevents the tutorial from playing every time
            firstGame = False
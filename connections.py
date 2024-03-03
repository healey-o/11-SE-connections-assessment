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
def get_random_categories():
    categories = {}

    while len(categories) < 4:#Picks 4 random categories
        random_choice = choice(list(ALL_CATEGORIES.keys()))
        
        if random_choice not in list(categories.keys()):
            categories[random_choice] = ALL_CATEGORIES[random_choice]

    return categories

#Combines all words in the given categories into a single list
def word_list_from_grid(grid:list):
    words = []

    for row in grid:
        for word in row:
            words.append(word)
    
    return words

#Takes the four categories and randomly places their words in a 4x4 grid
def randomize_grid(categories:dict):
    
    random_grid = []

    grid_words = []

    for category in categories:
        for word in categories[category]:
            grid_words.append(word)
    
    
    #Places these words in random positions in the list
    for y in range(4):
        row = []

        for x in range(4):
            selected_word = grid_words.pop(randint(0,len(grid_words)-1)) #popping ensures each word is used once
            row.append(selected_word)
        
        random_grid.append(row)
    
    return random_grid

#Displays the grid and associated info to the player
def display_grid(grid, found_categories):
    global lives

    print("\nCreate four groups of four!")

    grid_words = word_list_from_grid(grid)

    #Each grid 'tile' is the width of the longest word, plus a border of 3 spaces each side
    tile_width = len(max(grid_words, key=len)) + 6

    def draw_line():# Will add lines around each row of categories
        for i in range((tile_width+2)*4):#Add line between each row of categories
            print("-",end="")

    for row in grid:
        
        if grid.index(row) <= (len(found_categories) - 1): #When the line is displaying guessed categories, change text colour
            print("\u001b[32m")
        else:
            print("\u001b[37m")

        draw_line()
        print("\n")
        
        for word in row:
            print("|",end="")

            print(word.center(tile_width),end="") #Centres each word in the same sized box

            print("|",end="")
        
        print("\n")

        draw_line()

        

    print("\nMistakes remaining:", end="")#Lives counter
    for i in range(lives):
        print(" •",end="")
    print("\n")

#Edits the grid with any successfully guessed categories at the top
def redraw_grid(found_categories, grid):
    new_grid = []

    grid_words = word_list_from_grid(grid)

    if len(found_categories) > 0: #Adds found categories to the top of the new grid
        for found_category in found_categories:
            new_grid.append(found_categories[found_category])
            
            for word in found_categories[found_category]: #Removes the found category words from grid_words
                grid_words.pop(grid_words.index(word))

        for y in range(4-len(found_categories)): #Adds the remaining words to the grid
            row = []

            for x in range(4):
                selected_word = grid_words.pop(0) #Adds words that have not been guessed correctly back to the grid in the same order as before
                row.append(selected_word)
            
            new_grid.append(row)
    else:
        new_grid = grid

    return new_grid

#Prompts the player for their four guesses
def get_guesses():
    global lives

    guesses = []
    grid_words = word_list_from_grid(grid)

    while len(guesses) < 4:
        #All guesses are be made lowercase for easier matching
        guess = input("Enter a word from the grid:").lower()
        
        valid = False

        for word in grid_words:
            if guess == word.lower() and guess not in guesses:
                guesses.append(guess)
                valid = True

        if not valid:
            print("Sorry, that response is not valid. Please try again.")

        
    return guesses

#Checks the player's guesses against the four categories
def check_guesses(guesses, categories, found_categories):
    global lives

    valid = False

    for category in categories:
        if valid == False: #Repeats until a match is found or there are no more categories

            valid = True
            for word in categories[category]:
                if (word.lower() not in guesses) and valid:
                    valid = False
            
            if valid:
                found_categories[category] = categories[category]
                print(f"Correct! Found Category: {category}")
    
    if valid == False: #If the categories all returned false, lose a life
        lives -= 1
        print(f"Sorry, that is not correct.")


    return found_categories

#Checks if all categories have been found
def check_win(found_categories):

    if len(found_categories) == 4:
        return True
    else:
        return False

#Asks the player if they wish to play again or exit
def prompt_play_again():
    
    play_again = input("Do you want to play again? (Y/N)")

    if play_again.lower() in ["y","yes"]:
        return True
    elif play_again.lower() in ["n", "no", "get me out of here"]:
        return False
    else:
        print("Please enter Y or N.")
        return prompt_play_again()
    

#Main game loop - Displays the grid then prompts for and checks guesses
def game_loop(categories, grid, found_categories):

    display_grid(grid, found_categories)

    guesses = get_guesses()
    found_categories = check_guesses(guesses, categories, found_categories)


#Main script - initializes the variables, then runs the main game loop until the game ends.

if __name__ == "__main__":
    playing = True

    while playing:
        categories = get_random_categories()
        found_categories = {}

        grid = randomize_grid(categories)

        lives = 4 #Lives is used as a global variable as its value is often changed within functions

        game_won = False

        #Runs the game loop for the duration of the game
        while lives > 0 and not game_won:
            game_loop(categories, grid, found_categories)

            grid = redraw_grid(found_categories, grid) #Updates the grid variable after each loop

            game_won = check_win(found_categories) #Checks if the game is completed
        
        if game_won:
            print("Congratulations! You win!")
        else:
            print("Sorry, you have run out of lives.")
        
        playing = prompt_play_again()
    



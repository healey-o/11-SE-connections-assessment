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
    # "Brightness": ["Illuminate", "Radiate", "Gleam", "Shine"],
    # "Thinking Deeply": ["Ponder", "Contemplate", "Reflect", "Meditate"],
    # "Music Elements": ["Melody", "Harmony", "Rhythm", "Tune"],
    # "Speed": ["Brisk", "Swift", "Rapid", "Quick"],
    # "Shades of Blue": ["Azure", "Cerulean", "Cobalt", "Indigo"],
    # "Powerful Winds": ["Whirlwind", "Cyclone", "Tornado", "Hurricane"]
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
def word_list_from_categories(categories:dict):
    words = []

    for category in categories:
        for word in categories[category]:
            words.append(word)
    
    return words

#Takes the four categories and randomly places their words in a 4x4 grid
def randomize_grid(categories:dict):
    
    random_grid = []

    grid_words = word_list_from_categories(categories)
    
    
    #Places these words in random positions in the list
    for y in range(4):
        row = []

        for x in range(4):
            selected_word = grid_words.pop(randint(0,len(grid_words)-1)) #popping ensures each word is used once
            row.append(selected_word)
        
        random_grid.append(row)
    
    return random_grid

    

#Main game loop
def game_loop(categories, grid, lives, found_categories):
    display_grid(grid, lives, found_categories, categories)

    guesses = get_guesses(categories)
    found_categories = check_guesses(guesses, categories, found_categories)


#Displays the grid and associated info to the player
def display_grid(grid, lives, found_categories, categories):

    print("Create four groups of four!\n")

    words = word_list_from_categories(categories)

    #Each grid 'tile' is the width of the longest word, plus a border of 3 spaces each side
    tile_width = len(max(words, key=len)) + 6

    for i in range((tile_width+2)*4):
        print("-",end="")
    print("\n")

    for row in grid:
        for word in row:
            filler_len = (tile_width - len(word))

            print("|",end="")
            for i in range(math.floor(filler_len/2)):
                print(" ",end="")

            print(word,end="")

            for i in range(math.ceil(filler_len/2)):
                print(" ",end="")
            print("|",end="")
        
        print("\n")

        for i in range((tile_width+2)*4):
            print("-",end="")
        print("\n")

        

    print("Mistakes remaining:", end="")#Lives counter
    for i in range(lives):
        print(" •",end="")
    print("\n")

#Edits the grid with any successfully guessed categories at the top
def redraw_grid(categories, found_categories, grid):
    new_grid = []

    grid_words = word_list_from_categories(categories)

    if len(found_categories) > 0:
        for found_category in found_categories:
            new_grid.append(found_categories[found_category])
            for word in grid_words:
                if word in found_categories[found_category]:
                    grid_words.pop(grid_words.index(word))

        for y in range(4-len(found_categories)):
            row = []

            for x in range(4):
                selected_word = grid_words.pop(randint(0,len(grid_words)-1))
                row.append(selected_word)
            
            new_grid.append(row)
    else:
        new_grid = grid

    return new_grid


            

    

#Prompts the player for their four guesses
def get_guesses(categories):

    guesses = []
    grid_words = word_list_from_categories(categories)

    while len(guesses) < 4:
        #All guesses are be made lowercase for easier matching
        guess = input("Enter a word from the grid:").lower()
        
        valid = False

        for word in grid_words:
            if guess == word.lower():
                guesses.append(guess)
                valid = True

        if not valid:
            print("Sorry, that is not in the list. Please try again.")

        
    return guesses

#Checks the player's guesses against the four categories
def check_guesses(guesses, categories, found_categories):
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
    

#Main script - initializes the variables, then runs the main game loop until the game ends.

if __name__ == "__main__":

    categories = get_random_categories()
    found_categories = {}

    grid = randomize_grid(categories)

    lives = 4

    game_won = False

    while lives > 0 and not game_won:
        game_loop(categories, grid, lives, found_categories)

        grid = redraw_grid(categories, found_categories, grid)

        game_won = check_win(found_categories)
    



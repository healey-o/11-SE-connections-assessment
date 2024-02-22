from random import choice
from random import randint

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
def word_list_from_categories(categories):
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

    guesses = get_guesses()
    found_categories = check_guesses(guesses, categories, found_categories)

    check_win(found_categories)


#Displays the grid and associated info to the player
def display_grid(grid, lives, found_categories, categories):

    print("Create four groups of four!\n")

    for row in grid:
        for word in row:
            print(f"|{word}|",end="")
        print("\n")

    print("Mistakes remaining:", end="")#Lives counter
    for i in range(lives):
        print(" •",end="")
    print("\n")

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


    return found_categories

#Checks if all categories have been found
def check_win(found_categories):
    pass

#Asks the player if they wish to play again or exit
def prompt_play_again():
    pass
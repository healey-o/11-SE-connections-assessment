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
    "Brightness": ["Illuminate", "Radiate", "Gleam", "Shine"],
    "Thinking Deeply": ["Ponder", "Contemplate", "Reflect", "Meditate"],
    "Music Elements": ["Melody", "Harmony", "Rhythm", "Tune"],
    "Speed": ["Brisk", "Swift", "Rapid", "Quick"],
    "Shades of Blue": ["Azure", "Cerulean", "Cobalt", "Indigo"],
    "Powerful Winds": ["Whirlwind", "Cyclone", "Tornado", "Hurricane"]
    }

#Selects four random categories of words
def get_random_categories():
    categories = {}
    while len(categories) < 4:
        random_choice = choice(list(ALL_CATEGORIES.keys()))
        if random_choice not in list(categories.keys()):
            categories[random_choice] = ALL_CATEGORIES[random_choice]
    return categories

#Takes the four categories and randomly places their words in a 4x4 grid
def randomize_grid(categories:dict):
    words = []
    random_grid = []

    #Gets all words in the selected categories
    for category in categories:
        for word in categories[category]:
            words.append(word)
    
    #Places these words in random positions in the list
    for y in range(4):
        row = []

        for x in range(4):
            selected_word = words.pop(randint(0,len(words)-1))
            row.append(selected_word)
        
        random_grid.append(row)
    
    print(random_grid)
    return random_grid

randomize_grid(get_random_categories())

    

#Main game loop
def game_loop(categories, grid, lives, found_categories):
    display_grid(grid, lives, found_categories, categories)

    guesses = get_guesses()
    check_guesses(guesses, categories, found_categories)

    check_win(found_categories)


#Displays the grid and associated info to the player
def display_grid(grid, lives, found_categories, categories):
    pass

#Prompts the player for their four guesses
def get_guesses():
    pass

#Checks the player's guesses against the four categories
def check_guesses(guesses, categories, found_categories):
    pass

#Checks if all categories have been found
def check_win(found_categories):
    pass

#Asks the player if they wish to play again or exit
def prompt_play_again():
    pass
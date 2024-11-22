import requests
import random
import os
import json

the_leaderboard = "leaderboard.json"

def get_flags(): # gets the flags from the restcountries api and puts them into a dictionary
    response = requests.get("https://restcountries.com/v3.1/all")
    countries = response.text
    countries_data = json.loads(countries)  
    return {country['flags']['png']: country['name']['common'] for country in countries_data}


def random_flag(flags_dict): # picks a random flag from the dictionary after which it creates and opens the file to show the flag
    flag_url = random.choice(list(flags_dict.keys())) 
    country_name = flags_dict[flag_url]

    response = requests.get(flag_url)
    if response.status_code == 200:
        with open("flag.png", "wb") as file:
            file.write(response.content)

        os.startfile("flag.png") if os.name == 'nt' else os.system("xdg-open flag.png")
    return country_name 


def load_leaderboard(): # loads the leaderboard so that it can be edited
    try:
        with open(the_leaderboard, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_leaderboard(leaderboard): # writes the data into the leaderboard file
    with open(the_leaderboard, "w") as file:
        json.dump(leaderboard, file, indent=4)


def show_leaderboard(): # shows the current leaderboard from the json file neatly
    leaderboard = load_leaderboard()
    if leaderboard:
        print("*--- Leaderboard ---*")
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_leaderboard, start=1):
            print(f"{rank}. {player}: {score} points\n")
    else:
        print("No one's played yet...")


def game(username): # function that starts the game itself
    leaderboard = load_leaderboard()
    flags_dict = get_flags()

    high_score = leaderboard.get(username, 0)
    score = 0

    while True:
        country_name = random_flag(flags_dict)
        guess = input("Guess the name of this country: ").strip().lower()
        print("If you no longer want to play, type exit")

        if guess.lower() == "exit":
            break
        elif guess.lower() == country_name.lower():
            print("\nCorrect!\n")
            score += 1
        else:
            print(f"\nWrong! The correct answer was {country_name}.\n")
            print(f"Your score this round: {score}")
            print(f"Your high score is: {high_score}")
            break  

    if score > high_score:
        leaderboard[username] = score
        print(f"New high score for {username}: {score}")

    save_leaderboard(leaderboard)
    if os.path.exists("flag.png"):
        os.remove("flag.png")

def menu(): # prints the main menu for the user to interact with
    while True:
        print("\n*--------------------*")
        print("|  Guess the flag!   |")
        print("|  1. Start game     |")
        print("|  2. Leaderboard    |")
        print("|  3. Exit           |")
        print("*--------------------*")
        option = input("Choose an option: ").strip()

        if option == "1":
            username = input("Enter username: ").strip()
            game(username)
        elif option == "2":
            show_leaderboard()
        elif option == "3":
            print("See ya next time!")
            break
        else:
            print("Invalid. Try again.")

if __name__ == "__main__": # main function that starts the program
    menu()

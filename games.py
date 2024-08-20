import random
from colorama import Fore, Style, init
import pyfiglet
import json
from player import Player

# Initialize colorama for colored output
init(autoreset=True)

class Game:
    def __init__(self, num_ai):
        # Load settings from the JSON file
        with open("settings.json") as f:
            self.settings = json.load(f)
        
        # Create a list of players, with one human player and the specified number of AI players
        self.players = [Player(self.settings["human_name"], False)] + [Player(name, True) for name in self.settings["ai_names"]][:num_ai]
        self.num_ai = num_ai
        self.sum = 0             # Sum of all player guesses in the current round
        self.twist_num = 0       # The "twist" number for the current round
        self.player_alive_num = len(self.players)  # Number of players still in the game
        self.round_num = 1       # Current round number
        self.duplicate_guesses = []  # List to store duplicate guesses

    def about(self):
        # Print the current status of all players
        print(Fore.CYAN + Style.BRIGHT + "Player Status:")
        print(Fore.YELLOW + "-" * 60)
        for player in self.players:
            if player.alive:
                print(Fore.GREEN + f' [Name: {player.name} ; Points: {player.points} ; Guess: {player.guess}] ')
        print(Fore.YELLOW + "-" * 60)

    def guess(self):
        # Get guesses from all alive players for the current round
        print("")
        print(Fore.CYAN + Style.BRIGHT + f"Round {self.round_num}")
        self.duplicate_guesses = []  # Reset the list of duplicate guesses
        for player in self.players:
            if player.alive:
                if player.is_ai:
                    # AI player guesses a random number between 0 and 100
                    player.guess = random.randint(0, 100)
                else:
                    # Human player inputs their guess
                    while True:
                        try:
                            guess = int(input(Fore.BLUE + f"Enter your Guess {player.name} between [0,100]: "))
                            if 0 <= guess <= 100:
                                player.guess = guess
                                break
                            else:
                                print(Fore.RED + "Please enter a number between 0 and 100.")
                        except ValueError:
                            print(Fore.RED + "Invalid input! Please enter a number.")
            
            # Check for duplicate guesses
            if self.player_alive_num >= 4:
                if player.guess in [p.guess for p in self.players if p.alive and p != player]:
                    self.duplicate_guesses.append(player.guess)

    def twist(self):
        # Calculate the "twist" number for the current round
        self.sum = sum(player.guess for player in self.players if player.alive)
        avg = self.sum / self.player_alive_num
        self.twist_num = avg * 0.8

    def die(self):
        # Eliminate any players who have reached -10 points
        for player in self.players:
            if player.points <= -10 and player.alive:
                player.alive = False
                player.guess = 0
                self.player_alive_num -= 1
                print(Fore.RED + f"{player.name} has been eliminated!")

    def rounds(self):
        # Increment the round number
        self.round_num += 1

    def win(self):
        # Determine the winner of the current round
        winner = None
        min_diff = float('inf')
        
        if self.player_alive_num == 5:  # 5 players remaining
            for player in self.players:
                if player.alive:
                    diff = abs(player.guess - self.twist_num)
                    if diff < min_diff:
                        min_diff = diff
                        winner = player.name

            for player in self.players:
                if player.alive and player.name != winner:
                    player.points -= 1
           
        elif self.player_alive_num == 4:  # Placeholder for 4 players remaining
            None

        elif self.player_alive_num == 3:  # 3 players remaining
            # Invalidate duplicate guesses
            for duplicate_guess in set(self.duplicate_guesses):
                for player in self.players:
                    if player.alive and player.guess == duplicate_guess:
                        player.points -= 1
            
            # Find the winner
            for player in self.players:
                if player.alive:
                    diff = abs(player.guess - self.twist_num)
                    if diff < min_diff:
                        min_diff = diff
                        winner = player.name

            # Double the penalty for other players if the winner guessed the exact twist_num
            if min_diff == 0:
                for player in self.players:
                    if player.alive and player.name != winner:
                        player.points -= 2
            else:
                for player in self.players:
                    if player.alive and player.name != winner:
                        player.points -= 1

        else:  # Only 2 players remaining
            player1, player2 = [player for player in self.players if player.alive]
            if player1.guess == 0 and player2.guess == 100:
                winner = player2.name
            elif player1.guess == 100 and player2.guess == 0:
                winner = player1.name
            else:
                for player in self.players:
                    if player.alive:
                        if abs(player.guess - self.twist_num) < min_diff:
                            min_diff = abs(player.guess - self.twist_num)
                            winner = player.name

            # Update points for all alive players
            for player in self.players:
                if player.alive and player.name != winner:
                    player.points -= 1

        # Print the winner's name and the "twist" number
        if winner:
            print(Fore.GREEN + Style.BRIGHT + f"\n{winner} has won the round with the closest guess to {self.twist_num:.2f}!")

    def play(self):
        # Print the game title and welcome message
        title = pyfiglet.figlet_format("King of Diamonds", font="standard")
        print(Fore.YELLOW + title)
        print(Fore.CYAN + "Welcome to the King of Diamonds")
        print(Fore.YELLOW + "=" * 60)

        # Play rounds until only one player is left
        while self.player_alive_num > 1:
            self.die()
            if self.player_alive_num <= 1:
                break

            self.guess()
            self.twist()
            self.win()
            self.about()
            self.rounds()

            self.sum = 0
            self.twist_num = 0

        # Announce the grand winner
        self.grand_winner()

    def grand_winner(self):
        # Print the name of the grand winner
        for player in self.players:
            if player.alive:
                print(Fore.GREEN + Style.BRIGHT + f"\n{player.name.upper()} is the grand winner!")


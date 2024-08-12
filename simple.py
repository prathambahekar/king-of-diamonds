import random
import time

class Player:
    def __init__(self, name, is_ai):
        self.name = name         # Player's name
        self.points = 0          # Player's points
        self.guess = 0           # Player's guess for the current round
        self.is_ai = is_ai       # Boolean indicating whether the player is an AI or a human
        self.alive = True        # Boolean indicating whether the player is still in the game

class Game:
    def __init__(self, num_ai):
        # Create a list of players, with one human player and the specified number of AI players
        self.players = [Player("pam", False)] + [Player(name, True) for name in ["ash", "adi", "san", "becky"]][:num_ai]
        self.num_ai = num_ai
        self.sum = 0             # Sum of all player guesses in the current round
        self.twist_num = 0       # The "twist" number for the current round
        self.player_alive_num = len(self.players)  # Number of players still in the game
        self.round_num = 1       # Current round number
        self.duplicate_guesses = []  # List to store duplicate guesses
        self.new_rule_introduced = False  # Flag to track if a new rule was introduced in the current round

    def about(self):
        # Print the current status of all players
        print("Player Status:")
        print("-" * 60)
        for player in self.players:
            if player.alive:
                print(f' [Name: {player.name} ; Points: {player.points} ; Guess: {player.guess}] ')
        print("-" * 60)

    def guess(self):
        # Get guesses from all alive players for the current round
        print("")
        print(f"Round {self.round_num}")
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
                            guess = int(input(f"Enter your Guess {player.name} between [0,100]: "))
                            if 0 <= guess <= 100:
                                player.guess = guess
                                break
                            else:
                                print("Please enter a number between 0 and 100.")
                        except ValueError:
                            print("Invalid input! Please enter a number.")
            
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
                print(f"{player.name} has been eliminated!")
                self.introduce_new_rule()

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
        
        elif self.player_alive_num < 5:  # 4 or 3 players remaining
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
            # (only for 3 players remaining)
            if self.player_alive_num == 3 and min_diff == 0:
                for player in self.players:
                    if player.alive and player.name != winner:
                        player.points -= 2
            else:
                for player in self.players:
                    if player.alive and player.name != winner:
                        player.points -= 1

        else:  # 2 players remaining
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

            for player in self.players:
                if player.alive and player.name != winner:
                    player.points -= 1

        # Print the winner's name and the "twist" number
        if winner:
            print(f"\n{winner} has won the round with the closest guess to {self.twist_num:.2f}!")
            
    def introduce_new_rule(self):
        # Introduce a new rule if a player has been eliminated
        if self.player_alive_num == 4:
            print("\nNew Rule: If there are 2 people or more who choose the same number, that number becomes invalid, meaning they will lose a point even if the number is closest to 4/5ths the average.")
            self.new_rule_introduced = True
        elif self.player_alive_num == 3:
            print("\nNew Rule: If there is a person who chooses the exact correct number, the loser penalty is doubled.")
            self.new_rule_introduced = True
        elif self.player_alive_num == 2:
            print("\nNew Rule: If someone chooses 0, the player who chooses 100 is the winner.")
            self.new_rule_introduced = True

        

    def play(self):
        # Print the game title and welcome message
        # print(title)
        print("Welcome to the King of Diamonds")
        print("=" * 60)

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
                print(f"\n{player.name.upper()} is the grand winner!")

if __name__ == "__main__":
    # Create a new game with 4 AI players
    game = Game(num_ai=4)
    game.play()

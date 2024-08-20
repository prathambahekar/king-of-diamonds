class Player:
    def __init__(self, name, is_ai):
        self.name = name         # Player's name
        self.points = 0          # Player's points
        self.guess = 0           # Player's guess for the current round
        self.is_ai = is_ai       # Boolean indicating whether the player is an AI or a human
        self.alive = True        # Boolean indicating whether the player is still in the game

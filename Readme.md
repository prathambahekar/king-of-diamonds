# King of Diamonds

King of Diamonds is a guessing game where players, including AI, compete to guess a number closest to a calculated "twist" number. The game continues until only one player remains.

## Source
https://aliceinborderland.fandom.com/wiki/King_of_Diamonds


## Game Rules

1. **Players**: The game consists of one human player and a specified number of AI players.
2. **Rounds**: Each round, players guess a number between 0 and 100.
3. **Twist Number**: The twist number is calculated as 80% of the average of all guesses.
4. **Elimination**: Players with points less than or equal to -10 are eliminated.
5. **Winning a Round**: The player with the guess closest to the twist number wins the round.
6. **End of Game**: The game continues until only one player remains, who is declared the grand winner.

## Installation

1. Clone the repository.
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## How to Play

1. Run the game:
    ```sh
    python main.py
    ```
2. Follow the on-screen instructions to input your guesses.

## File Structure

- [__init__.py](http://_vscodecontentref_/0): Initializes the package.
- [games.py](http://_vscodecontentref_/1): Contains the `Game` class which implements the game logic.
- [main.py](http://_vscodecontentref_/2): Entry point to start the game.
- [player.py](http://_vscodecontentref_/3): Contains the `Player` class which represents a player in the game.
- [settings.json](http://_vscodecontentref_/4): Configuration file containing player names.

## Configuration

You can customize the player names in the [settings.json](http://_vscodecontentref_/5) file:
```json
{
    "human_name": "player 1",
    "ai_names": ["player 2", "player 3", "player 4", "player 5"]
}
```

## Image

![image](https://github.com/user-attachments/assets/97e967b5-c168-4484-a8fa-62bd0e4395c9)


#Hello, Pradnya Chute this side. Will be contributing towards this project!
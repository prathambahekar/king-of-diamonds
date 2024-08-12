#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_PLAYERS 5
#define MAX_NAME_LENGTH 50
#define MAX_DUPLICATES 100

typedef struct {
    char name[MAX_NAME_LENGTH];
    int points;
    int guess;
    int is_ai;
    int alive;
} Player;

typedef struct {
    Player players[MAX_PLAYERS];
    int num_players;
    int sum;
    double twist_num;
    int player_alive_num;
    int round_num;
    int duplicate_guesses[MAX_DUPLICATES];
    int num_duplicates;
    int new_rule_introduced;
} Game;

void initialize_game(Game *game, int num_ai);
void print_about(Game *game);
void get_guesses(Game *game);
void calculate_twist(Game *game);
void eliminate_players(Game *game);
void increment_round(Game *game);
void determine_winner(Game *game);
void introduce_new_rule(Game *game);
void play_game(Game *game);
void announce_grand_winner(Game *game);

int main() {
    srand(time(NULL));
    Game game;
    initialize_game(&game, 4);
    play_game(&game);
    return 0;
}

void initialize_game(Game *game, int num_ai) {
    strcpy(game->players[0].name, "pam");
    game->players[0].is_ai = 0;
    game->players[0].points = 0;
    game->players[0].guess = 0;
    game->players[0].alive = 1;

    char *ai_names[] = {"ash", "adi", "san", "becky"};
    for (int i = 1; i <= num_ai; i++) {
        strcpy(game->players[i].name, ai_names[i - 1]);
        game->players[i].is_ai = 1;
        game->players[i].points = 0;
        game->players[i].guess = 0;
        game->players[i].alive = 1;
    }

    game->num_players = num_ai + 1;
    game->sum = 0;
    game->twist_num = 0.0;
    game->player_alive_num = game->num_players;
    game->round_num = 1;
    game->num_duplicates = 0;
    game->new_rule_introduced = 0;
}

void print_about(Game *game) {
    printf("Player Status:\n");
    printf("------------------------------------------------------------\n");
    for (int i = 0; i < game->num_players; i++) {
        if (game->players[i].alive) {
            printf(" [Name: %s ; Points: %d ; Guess: %d] \n",
                   game->players[i].name,
                   game->players[i].points,
                   game->players[i].guess);
        }
    }
    printf("------------------------------------------------------------\n");
}

void get_guesses(Game *game) {
    printf("\nRound %d\n", game->round_num);
    game->num_duplicates = 0;
    for (int i = 0; i < game->num_players; i++) {
        if (game->players[i].alive) {
            if (game->players[i].is_ai) {
                game->players[i].guess = rand() % 101;
                printf("%s (AI) guessed: %d\n", game->players[i].name, game->players[i].guess);
            } else {
                int valid_input = 0;
                while (!valid_input) {
                    printf("Enter your Guess %s between [0,100]: ", game->players[i].name);
                    if (scanf("%d", &game->players[i].guess) != 1) {
                        while (getchar() != '\n'); // Clear input buffer
                        printf("Invalid input! Please enter a number.\n");
                    } else if (game->players[i].guess < 0 || game->players[i].guess > 100) {
                        printf("Please enter a number between 0 and 100.\n");
                    } else {
                        valid_input = 1;
                    }
                }
            }
        }
    }

    // Check for duplicate guesses
    if (game->player_alive_num >= 4) {
        for (int i = 0; i < game->num_players; i++) {
            if (game->players[i].alive) {
                for (int j = i + 1; j < game->num_players; j++) {
                    if (game->players[j].alive && game->players[i].guess == game->players[j].guess) {
                        game->duplicate_guesses[game->num_duplicates++] = game->players[i].guess;
                    }
                }
            }
        }
    }
}

void calculate_twist(Game *game) {
    game->sum = 0;
    for (int i = 0; i < game->num_players; i++) {
        if (game->players[i].alive) {
            game->sum += game->players[i].guess;
        }
    }
    double avg = (double)game->sum / game->player_alive_num;
    game->twist_num = avg * 0.8;
}

void eliminate_players(Game *game) {
    for (int i = 0; i < game->num_players; i++) {
        if (game->players[i].points <= -10 && game->players[i].alive) {
            game->players[i].alive = 0;
            game->players[i].guess = 0;
            game->player_alive_num--;
            printf("%s has been eliminated!\n", game->players[i].name);
            introduce_new_rule(game);
        }
    }
}

void increment_round(Game *game) {
    game->round_num++;
}

void determine_winner(Game *game) {
    char winner[MAX_NAME_LENGTH];
    double min_diff = 1e9;
    int winner_found = 0;

    if (game->player_alive_num == 5) {
        for (int i = 0; i < game->num_players; i++) {
            if (game->players[i].alive) {
                double diff = abs(game->players[i].guess - game->twist_num);
                if (diff < min_diff) {
                    min_diff = diff;
                    strcpy(winner, game->players[i].name);
                    winner_found = 1;
                }
            }
        }

        for (int i = 0; i < game->num_players; i++) {
            if (game->players[i].alive && strcmp(game->players[i].name, winner) != 0) {
                game->players[i].points -= 1;
            }
        }

    } else if (game->player_alive_num < 5 && game->player_alive_num >= 3) {
        // Invalidate duplicate guesses
        for (int d = 0; d < game->num_duplicates; d++) {
            int duplicate_guess = game->duplicate_guesses[d];
            for (int i = 0; i < game->num_players; i++) {
                if (game->players[i].alive && game->players[i].guess == duplicate_guess) {
                    game->players[i].points -= 1;
                }
            }
        }

        // Find the winner
        for (int i = 0; i < game->num_players; i++) {
            if (game->players[i].alive) {
                double diff = abs(game->players[i].guess - game->twist_num);
                if (diff < min_diff) {
                    min_diff = diff;
                    strcpy(winner, game->players[i].name);
                    winner_found = 1;
                }
            }
        }

        if (game->player_alive_num == 3 && min_diff == 0) {
            for (int i = 0; i < game->num_players; i++) {
                if (game->players[i].alive && strcmp(game->players[i].name, winner) != 0) {
                    game->players[i].points -= 2;
                }
            }
        } else {
            for (int i = 0; i < game->num_players; i++) {
                if (game->players[i].alive && strcmp(game->players[i].name, winner) != 0) {
                    game->players[i].points -= 1;
                }
            }
        }

    } else { // 2 players remaining
        Player *player1 = NULL;
        Player *player2 = NULL;
        for (int i = 0; i < game->num_players; i++) {
            if (game->players[i].alive) {
                if (!player1) {
                    player1 = &game->players[i];
                } else {
                    player2 = &game->players[i];
                }
            }
        }

        if (player1->guess == 0 && player2->guess == 100) {
            strcpy(winner, player2->name);
            winner_found = 1;
        } else if (player1->guess == 100 && player2->guess == 0) {
            strcpy(winner, player1->name);
            winner_found = 1;
        } else {
            for (int i = 0; i < game->num_players; i++) {
                if (game->players[i].alive) {
                    double diff = abs(game->players[i].guess - game->twist_num);
                    if (diff < min_diff) {
                        min_diff = diff;
                        strcpy(winner, game->players[i].name);
                        winner_found = 1;
                    }
                }
            }
        }

        for (int i = 0; i < game->num_players; i++) {
            if (game->players[i].alive && strcmp(game->players[i].name, winner) != 0) {
                game->players[i].points -= 1;
            }
        }
    }

    if (winner_found) {
        printf("\n%s has won the round with the closest guess to %.2f!\n", winner, game->twist_num);
    }
}

void introduce_new_rule(Game *game) {
    if (game->player_alive_num == 4 && !game->new_rule_introduced) {
        printf("\nNew Rule: If there are 2 people or more who choose the same number, that number becomes invalid, meaning they will lose a point even if the number is closest to 4/5ths the average.\n");
        game->new_rule_introduced = 1;
    } else if (game->player_alive_num == 3 && !game->new_rule_introduced) {
        printf("\nNew Rule: If there is a person who chooses the exact correct number, the loser penalty is doubled.\n");
        game->new_rule_introduced = 1;
    } else if (game->player_alive_num == 2 && !game->new_rule_introduced) {
        printf("\nNew Rule: If someone chooses 0, the player who chooses 100 is the winner.\n");
        game->new_rule_introduced = 1;
    }
}

void play_game(Game *game) {
    printf("Welcome to the King of Diamonds\n");
    printf("============================================================\n");

    while (game->player_alive_num > 1) {
        eliminate_players(game);
        if (game->player_alive_num <= 1) {
            break;
        }

        get_guesses(game);
        calculate_twist(game);
        determine_winner(game);
        print_about(game);
        increment_round(game);

        game->sum = 0;
        game->twist_num = 0.0;
    }

    announce_grand_winner(game);
}

void announce_grand_winner(Game *game) {
    for (int i = 0; i < game->num_players; i++) {
        if (game->players[i].alive) {
            printf("\n%s is the grand winner!\n", strupr(game->players[i].name));
        }
    }
}

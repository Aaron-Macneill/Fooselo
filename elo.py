import pickle
import os
import datetime
import matplotlib.pyplot as plt
import random

BANNERS = ["""
 _____ _
| ____| | ___
|  _| | |/ _ \\
| |___| | (_) |
|_____|_|\___/
"""]


class Player():
    def __init__(self, name):
        self.name = name
        self.games = [1500]
        self.score = 1500
        self.scores_over_time = [1500]

    def __add__(self, opponent):
        """If you win"""
        self.win(opponent)
    
    def __sub__(self, opponent):
        self.loss(opponent)

    def __repr__(self):
        return f"{self.name}: {round(self.score, 2)}"

    def __str__(self):
        return f"{self.name}: {round(self.score, 2)}"

    def win(self, opponent):
        opponent_score = opponent.get_score()
        self.games.append(opponent_score + 400)
        # update the opponent's thing
        opponent.games.append(self.score - 400)
        self.__update_score__()
        opponent.__update_score__()

    def gains(self, opponent):
        opponent_score = opponent.get_score()
        my_games = self.games.copy()
        my_games.append(opponent_score + 400)
        return sum(my_games) / len(my_games)

    def loss(self, opponent):
        opponent_score = opponent.get_score()
        self.games.append(opponent_score - 400)
        # update the opponent's thing
        opponent.games.append(self.score + 400)

    def tie(self, opponent):
        opponent_score = opponent.get_score()
        self.games.append(opponent_score)
    
    def __update_score__(self):
        self.score = sum(self.games) / len(self.games)
        self.scores_over_time.append(self.score)

    def get_score(self):
        self.__update_score__()
        return self.score

def demo():
    ben = Player("Benedict")
    max = Player("Maximillion")

    breakpoint()

    print("Before game:")
    print(f"Ben: {ben.get_score()} Max: {max.get_score()}")

    print("After game:")
    ben.win(max)
    #maximillion.loss(benedict)
    print(f"Ben: {ben.get_score()} Max: {max.get_score()}")


def save_db(db, db_fname="db.pickle"):
    with open(db_fname, 'wb') as f:
        pickle.dump(db, f)

def load_db(db_fname="db.pickle"):
    if os.path.exists(db_fname):
        with open(db_fname, 'rb') as f:
            return pickle.load(f)
    else:
        return {}, []

def disp_scores(players, des_names=False):
    if des_names == False:
        des_names = players.keys()
    for p in des_names:
        print(players[p])

def main():
    print(random.choice(BANNERS))


    players, history = load_db()
    while True:
        res = input("~> ")
        timestamp = datetime.datetime.now()
        history.append((timestamp, res))

        if res.startswith("register"):
            new_player_names = res.split(" ")[1:]
            for npn in new_player_names:
                print(f"Ok. Registering player: {npn}")
                players[npn] = Player(npn)
        
        elif res.startswith("win"):
            winner_name, loser_name = res.split(" ")[1:]
            
            winp_0 = round(players[winner_name].score, 2)
            losp_0 = round(players[loser_name].score, 2)
            
            players[winner_name].win(players[loser_name])

            winp_1 = round(players[winner_name].score, 2)
            losp_1 = round(players[loser_name].score, 2)

            print(f"{winner_name}: {winp_0}->{winp_1} ✔️")
            print(f"{loser_name}: {losp_0}->{losp_1} ❌")
        
        elif res == "scores":
            print("❄️ --- Scores --- ❄️")
            disp_scores(players)
            print ("--------------------")

        elif res == "exit":
            exit()

        elif res == "history":
            for entry in history:
                e_timestamp = entry[0].strftime("%Y-%m-%d %H:%M:%S")
                e_command = entry[1]
                print(f"{e_timestamp} ~> {e_command}")

        elif res.startswith("pot"):
            pot_name = res.split(' ')[1]
            pot_player = players[pot_name]
            print(f"{pot_name}'s current score: {round(pot_player.score, 2)}")
            print(f"--- {pot_name}'s Potential Gains ---")
            for player_name in players:
                if player_name != pot_name:
                    this_player = players[player_name]
                    gained_elo = round(pot_player.gains(this_player), 2)
                    if gained_elo > pot_player.score:
                        denote_char = "✔️"
                    elif gained_elo == pot_player.score:
                        denote_char = "🟨"
                    elif gained_elo < pot_player.score:
                        denote_char = "❌"
                    print(f"{player_name} yields {gained_elo} {denote_char}")
        
        elif res.startswith("predict"):
            names = res.split(" ")[1:]
            p1 = names[0]
            p2 = names[1]
            r1 = players[p1].score
            r2 = players[p2].score
            E1 = 1/(1+10**((r2-r1)/400))
            E2 = 1/(1+10**((r1-r2)/400))
            print(f"Probability of {p1} winning against {p2} is {round(100*E1, 2)}%.")

        elif res in players:
            disp_scores(players, [res])
            plt.plot(players[res].scores_over_time, '--ko')
            plt.plot(players[res].games, '--ro')
            plt.legend([f"{res}'s Score Over Time", "Game points"])
            plt.title(f"{res}'s Score")
            plt.xlabel("Game (#)")
            plt.ylabel("Score (Elo)")
            plt.show()
        elif res == "upupupdowndowndown":
            breakpoint()
        else:
            print("Invalid command.")

        save_db([players, history])

        


if __name__ == '__main__':
    main()
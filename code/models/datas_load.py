from code.models.player import Player
from code.models.tournament import Tournament

def load_sample_datas():

    def adding_8_players():
        Player("Farse", "Bertrand", "18/04/1990", "H", 4)
        Player("Godran", "Jean", "18/04/1995", "H", 2)
        Player("Gadzish", "Sven", "18/04/1997", "H", 3)
        Player("Bernard", "Martin", "18/04/1997", "H", 5)
        Player("Rousseau", "Jacques", "18/04/1997", "H", 7)
        Player("Noire", "Arnold", "18/04/1997", "H", 9)
        Player("De Galice", "François", "18/04/1980", "H", 10)
        Player("Kasparov", "Garry", "18/04/1956", "H", 1)
        pass

    adding_8_players()

    player_list = [Player._registry[0],Player._registry[1],Player._registry[2],Player._registry[3],
                   Player._registry[4],Player._registry[5],Player._registry[6],Player._registry[7]]

    def add_1_tournament():
        Tournament("TEST1", "PARIS", "20/10/2020", "20/10/2020",4,player_list,"Blitz","Une note")

    add_1_tournament()

    print(f"\n-- We have loaded {len(Player._registry)} "
          f"players and {len(Tournament._registry)} tournament(s)\n")

    return


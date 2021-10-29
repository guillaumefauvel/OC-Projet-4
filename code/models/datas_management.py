from code.models.player import Player
from code.models.tournament import Tournament
from tinydb import TinyDB

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

def player_maker(dict_to_transform):
    """ Create player objects
    Arg : The json file containing the player_infos
    """
    serialized_datas = []
    for value in dict_to_transform:
        serialized_datas.append(value)
    # dict_to_transform.clear()
    for value in serialized_datas:
        name = value['name']
        first_name = value['first_name']
        birthday = value['birthday']
        gender = value['gender']
        ranking = value['ranking']
        Player(name, first_name, birthday, gender, ranking)

def save_data():
    """ Save the player data into a json file """
    database = TinyDB('database.json', indent=1)
    player_table = database.purge_table("Player")
    player_table = database.table("Player")
    player_table.insert_multiple(Player._serialized_registry)
    pass

def load_from_save():
    """ Create players from the json file """
    database = TinyDB('database.json', indent=1)
    player_table = database.table("Player")
    player_maker(player_table.all())
    print("The datas has been loaded")


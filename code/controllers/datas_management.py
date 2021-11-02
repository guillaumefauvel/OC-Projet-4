from models.player import Player
from models.tournament import Tournament
from tinydb import TinyDB

def load_sample_datas():
    """ Load the informations needed to try the tournament mechanics """
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

    player_list = ["Garry Kasparov","Jean Godran","Bertrand Farse","Sven Gadzish","Arnold Noire","Martin Bernard",
                   "Jacques Rousseau","François De Galice"]

    def add_1_tournament():
        Tournament("TEST1", "PARIS", "20/10/2020", "20/10/2020",4,player_list,"Blitz","Une note")

    add_1_tournament()

    print(f"\n-- We have loaded {len(Player._registry)} "
          f"players and {len(Tournament._registry)} tournament(s)\n")

    return

def player_maker(dict_to_transform):
    """ Create player objects
    Arg : A dict of serialized datas
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
    database.purge_table("Player")
    database.purge_table("Tournament")
    player_table = database.table("Player")
    player_table.insert_multiple(Player._serialized_registry)
    tournament_table = database.table('Tournament')
    tournament_table.insert_multiple(Tournament._serialized_registry)

    return

def load_from_save():
    """ Recreate player and tournament object from the json file """
    database = TinyDB('database.json', indent=1)
    player_table = database.table("Player")
    tournament_table = database.table("Tournament")

    player_maker(player_table.all())
    tournament_maker(tournament_table.all())

    return

def tournament_maker(dict_to_transform):
    """ Create tournament object(s)
        Arg : A dict of serialized datas
        """
    for value in dict_to_transform:
        name = value['name']
        location = value['location']
        start_date = value['start_date']
        end_date = value['end_date']
        num_of_round = value['num_of_round']
        selected_players = value['selected_players']
        game_type = value['game_type']
        notes = value['notes']
        Tournament(name, location, start_date, end_date, num_of_round,
                   selected_players, game_type, notes)

    return


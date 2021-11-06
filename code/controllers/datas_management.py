from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from tinydb import TinyDB, Query

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
        try:
            player = Player._registry[-1]
            player.num_of_wins = value['num_of_wins']
            player.num_of_losses = value['num_of_losses']
            player.num_of_draw = value['num_of_draw']
            player.winloss_ratio = value['win_loss_ratio']
            player.num_of_match = value['num_of_match']
            player.num_of_tournaments = value['num_of_tournaments']
        except:
            pass

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
    tournament_created = []

    for value in dict_to_transform:
        if value['name'] not in tournament_created:
            tournament_created.append(value['name'])
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

            # Making the round and the match
            for index in range(1,num_of_round+1):
                duel_list = value['serialized_object'][str(index)][0]
                results = value['serialized_object'][str(index)][1]
                Tournament._registry[-1].object_dict[index] = Round(duel_list)
                Tournament._registry[-1].object_dict[index].make_match()
                # Adding the score to the round
                for match, result in zip(Match._registry[-num_of_round:],results):
                    match.winner = result
            # Adding the scoreboard
            Tournament._registry[-1].scoreboard = value['scoreboard']

def serializing_tournament_player():

    players_reference_list = []
    tournaments_name_list = []
    for player in Player._registry:
        if player.reference not in players_reference_list:
            players_reference_list.append(player.reference)
            player.update_player_datas()
    for tournament in Tournament._registry:
        if tournament.name not in tournaments_name_list:
            tournaments_name_list.append(tournament.name)
            tournament.serialized_the_object()
    return

# -DEVonly
def delete_duplicates():
    """ Remove tournament duplicated from the database """

    database = TinyDB('database.json', indent=1)
    tournament_table = database.table("Tournament")
    list_of_tournament_names = []
    for value in tournament_table:
        if value['name'] not in list_of_tournament_names:
            list_of_tournament_names.append(value['name'])
        else:
            tournament_table.remove(Query().name == value['name'])
            print("Already in")
    pass

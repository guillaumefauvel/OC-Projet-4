from models.player import Player
from models.tournament import Tournament
from models.round import Round
from models.match import Match

from tinydb import TinyDB
from datetime import datetime


def save_data():
    """ Save the player and the tournament data into a json file """
    database = TinyDB('database.json', indent=1)
    database.purge_table("Player")
    database.purge_table("Tournament")

    player_table = database.table("Player")
    player_table.insert_multiple(Player._serialized_registry)

    tournament_table = database.table('Tournament')
    tournament_table.insert_multiple(Tournament._serialized_registry)
    return


def serializing_tournament_player():
    """ Serialize the players and the tournaments"""

    for player in Player._registry:
        player.update_player_datas()

    for tournament in Tournament._registry:
        tournament.serialized_the_object()

    return


def player_maker(dict_to_transform):
    """ Create player objects
    Arg : A dict of serialized datas
    """
    serialized_datas = []
    for value in dict_to_transform:
        serialized_datas.append(value)

    for value in serialized_datas:
        name = value['name']
        first_name = value['first_name']
        birthday = value['birthday']
        gender = value['gender']
        ranking = value['ranking']
        Player(name, first_name, birthday, gender, ranking)
        player = Player._registry[-1]
        player.num_of_wins = value['num_of_wins']
        player.num_of_losses = value['num_of_losses']
        player.num_of_draw = value['num_of_draw']
        player.winloss_ratio = value['win_loss_ratio']
        player.num_of_match = value['num_of_match']
        player.num_of_tournaments = value['num_of_tournaments']


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
            for index in range(1, len(value['serialized_object'])+1):
                duel_list = value['serialized_object'][str(index)][0]
                results = value['serialized_object'][str(index)][1]
                start_times = value['serialized_object'][str(index)][2]
                end_times = value['serialized_object'][str(index)][3]

                Tournament._registry[-1].object_dict[index] = Round(duel_list)
                round_start_time = value['serialized_object'][str(index)][4][0]
                round_end_time = value['serialized_object'][str(index)][4][1]
                Round._registry[-1].start_time = datetime.strptime(round_start_time, '%d-%b-%Y (%H:%M:%S.%f)')
                Round._registry[-1].end_time = datetime.strptime(round_end_time, '%d-%b-%Y (%H:%M:%S.%f)')

                Tournament._registry[-1].object_dict[index].make_match()

                for match, result, start_time, end_time in zip(Match._registry[-len(results):],
                                                               results, start_times, end_times):
                    match.winner = result
                    match.start_time = datetime.strptime(start_time, '%d-%b-%Y (%H:%M:%S.%f)')
                    match.end_time = datetime.strptime(end_time, '%d-%b-%Y (%H:%M:%S.%f)')

            # Adding the scoreboard
            Tournament._registry[-1].scoreboard = value['scoreboard']


def load_from_save():
    """ Recreate player and tournament object from the json file """
    database = TinyDB('database.json', indent=1)
    player_table = database.table("Player")
    tournament_table = database.table("Tournament")
    player_maker(player_table.all())
    tournament_maker(tournament_table.all())

    return

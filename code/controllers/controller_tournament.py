from models.player import Player
from models.match import Match
from views.view_tournament import show_duel, asking_match_result, show_scoreboard, show_score, asking_end_match

def make_player_dict():
    """Explore all the player object.
    Return a dictionnary : key=index, value=player_object """
    reference_dict = {}
    for index, player in zip(range(1, len(Player._registry)+1), Player._registry):
        reference_dict[index] = player

    return reference_dict

def convert_to_reference(list_of_player_object):
    """ Convert a list of player object into a list of reference """
    players_references = []
    for object in list_of_player_object:
        players_references.append(object.reference)
    return players_references


def convert_to_player_object(list_of_player_reference):
    """ Convert a list of player reference into a list of player object """
    list_of_player_object = []
    for player_ref in list_of_player_reference:
        for player_object in Player._registry:
            if player_ref == player_object.reference:
                list_of_player_object.append(player_object)
    return list_of_player_object


def round_conversion(list_of_round):
    """ Convert a list of round object into a serialized dict
    arg : a list of round object
    return : a dict containing the duel list of a round and the result of those matchs
    These informations are in order to serialized the content of the tournament """
    serialized_dict = {}

    for value, index in zip(list_of_round,range(1,len(list_of_round)+1)):
        serialized_dict[index] = [list_of_round[value].duel_list,
                                  [x.winner for x in list_of_round[value].attached_match]]

    return serialized_dict

def player_researcher(*player_reference):
    """ Return the objects of n number of player / Args : players references --> Controler ? """

    researched_results = []
    for player in player_reference:
        for found_player in Player._registry:
            if found_player.reference == player:
                researched_results.append(found_player)
    return researched_results

def adding_result_match(results, num_of_match):
    """ Adding the result of the matchs into the matchs objects
     Args : a list of the matchs results, the number of matches"""

    for match, result in zip(Match._registry[-num_of_match:], results):
        match.winner = result
    pass

def adding_time_match(match_label_list, num_of_match):
    """ Adding the start_time and the end_time to the match object
    Args : a list of start_time/end_time, the number of match"""

    for match in Match._registry[-num_of_match:]:
        for time_infos in match_label_list:
            player_1 = match_label_list[time_infos][0][0]['match'][0]
            if match.player_1 == player_1:
                match.start_time = match_label_list[time_infos][0][1]['start_time']
                match.end_time = match_label_list[time_infos][1]
    return

def updating_players_stats(tournament_object):
    """ Update the players stats by using the result of the tournament
    Arg : The tournament object """

    serialized_tournament = tournament_object.serialized_object
    for value in serialized_tournament:
        duel_list = serialized_tournament[value][0]
        result_list = serialized_tournament[value][1]
        for match, result in zip(duel_list, result_list):
            if result == "1":
                player_researcher(match[0])[0].num_of_wins += 1
                player_researcher(match[1])[0].num_of_losses += 1

            elif result == "2":
                player_researcher(match[1])[0].num_of_wins += 1
                player_researcher(match[0])[0].num_of_losses += 1

            else:
                player_researcher(match[1])[0].num_of_draw += 1
                player_researcher(match[0])[0].num_of_draw += 1


    players_list = tournament_object._serialized_registry[-1]['selected_players']

    for player in players_list:
        player_object = player_researcher(player)[0]
        player_object.num_of_tournaments += 1
        num_of_match = player_object.num_of_wins + player_object.num_of_losses\
                       + player_object.num_of_draw
        player_object.num_of_match = num_of_match
        try:
            player_object.winloss_ratio = round(player_object.num_of_wins / player_object.num_of_losses,2)
        except:
            player_object.winloss_ratio = 0
        player_object.update_player_datas()

    return

def updating_general_rank():
    """ Use the player registry in order to reorganize the player's rank
    the 1st player is the one with the most victory """

    players_dict = {}

    for player, index in zip(Player._registry, range(1, len(Player._registry) + 1)):
        players_dict[index] = [player.reference, player.ranking, player.num_of_wins]

    sorted_by_wins = dict(sorted(players_dict.items(), key=lambda item: item[1][2], reverse=True))

    for player, rank in zip(sorted_by_wins,range(1,len(Player._registry)+1)):
        player_researcher(sorted_by_wins[player][0])[0].ranking = rank


    return

def launch_from_controller(tournament_object):
    """ Hold the logic behind a tournament
    Arg : A tournament object """


    # Sort the player by making an ordered dict
    tournament_object.return_ranking()
    # Generate the first series of duel thanks to the scoreboard
    list_of_duel = tournament_object.first_draw()
    # Show the user the list of duels
    show_duel(list_of_duel)
    # Ask the user to end the match
    time_informations = asking_end_match(list_of_duel)
    # Ask the user the result of the match
    results = asking_match_result(list_of_duel)
    # Add those result to the match object
    adding_result_match(results, len(results))
    adding_time_match(time_informations, len(time_informations))
    # Use these matchs objects to update the scoreboard
    tournament_object.updating_scoreboard_score(1)
    # Sort the scoreboard
    tournament_object.sort_score_rank()
    # Show the scoreboard
    show_score(sorted(tournament_object.scoreboard.values(), key=lambda k: k['score'], reverse=True), 1)
    # Iterate on the number of round left
    for number_of_round in range(2, tournament_object.num_of_round + 1):

        # Generate the next series of duel thanks to the scoreboard
        list_of_duel = tournament_object.generating_other_draw(number_of_round)
        tournament_object.updating_scoreboard_associations(list_of_duel)
        show_duel(list_of_duel)
        results = asking_match_result(list_of_duel)
        adding_result_match(results, len(results))
        adding_time_match(time_informations, len(time_informations))
        tournament_object.updating_scoreboard_score(number_of_round)
        tournament_object.sort_score_rank()
        show_score(sorted(tournament_object.scoreboard.values(), key=lambda k: k['score'],reverse=True),number_of_round)

    tournament_object.serialized_the_object()
    updating_players_stats(tournament_object)
    updating_general_rank()
    tournament_object.serialized_the_object()

    return

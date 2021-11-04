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

    for match, result in zip(Match._registry[-num_of_match:], results):
        match.winner = result
    pass

def adding_time_match(match_label_list, num_of_match):

    for match in Match._registry[-num_of_match:]:
        for time_infos in match_label_list:
            # player_1 = match_label_list[time_infos][0][0]['match'][0]
            player_1 = str(match_label_list[time_infos][0][0]['match'][0])
            if match.player_1 == player_1:
                match.start_time = match_label_list[time_infos][0][1]['start_time']
                match.end_time = match_label_list[time_infos][1]

    return

def launch_from_controller(tournament_object):

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
        tournament_object.updating_scoreboard_score(number_of_round)
        tournament_object.sort_score_rank()
        show_score(sorted(tournament_object.scoreboard.values(), key=lambda k: k['score'],reverse=True),number_of_round)

    tournament_object.serialized_the_object()
    # for value in tournament_object.serialized_object:
    #     print(tournament_object.serialized_object[value])
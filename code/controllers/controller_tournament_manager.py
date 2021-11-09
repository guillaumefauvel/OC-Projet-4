from models.player import Player
from models.match import Match
from models.tournament import Tournament

from views.view_tournament import show_duel, asking_match_result, show_scoreboard, show_score, asking_end_match
from views.view_tournament_manager import ask_choice, show_tournament_list
from views import view_menu, view_tournament_manager, view_players_manager

import controllers.controller_menu
from tinydb import TinyDB, Query


def tournament_manager():
    """ Show the user the possibilities and gathered his answer.
    He is redirected in order to fulfill is choice."""

    answer = ask_choice()
    if answer == "1":
        tournament_launching()
    elif answer == "2":
        controllers.controller_menu.menu_loop(delete_tournament)
        pass
    return


def tournament_launching():
    """ Create and launch a new tournament """

    player_dict = make_player_dict()
    name, location, start_date, end_date, num_of_round, selected_players, game_type, notes \
        = view_tournament_manager.new_tournament(player_dict)

    selected_players = convert_to_reference(selected_players)
    Tournament(name, location, start_date, end_date, num_of_round, selected_players, game_type, notes)

    last_tournament = (Tournament._registry[-1])
    launch_from_controller(last_tournament)

    return


def make_player_dict():
    """Explore all the player object.
    Return a dictionnary : key=index, value=player_object """
    reference_dict = {}
    for index, player in zip(range(1, len(Player._registry)+1), Player._registry):
        reference_dict[index] = player

    return reference_dict


def make_tournament_dict():
    """ Make a dictionnary of tournament
    Return : A dictionnary with key=index, value=tournament_name"""

    tournament_dict = {}

    for index, tournament in zip(range(1, len(Tournament._registry)+1), Tournament._registry):
        tournament_dict[index] = tournament.name

    return tournament_dict


def convert_to_reference(list_of_player_object):
    """ Convert a list of player object into a list of reference
    Arg : A list of player object
    Return : A list of player reference (ie : 'Garry Kasparov') """

    players_references = []
    for player_object in list_of_player_object:
        players_references.append(player_object.reference)

    return players_references


def player_researcher(*player_reference):
    """ Return the objects of n number of player
    Args : players references """

    researched_results = []
    for player in player_reference:
        for found_player in Player._registry:
            if found_player.reference == player:
                researched_results.append(found_player)
    return researched_results


def adding_result_match(results):
    """ Adding the result of the matchs into the matchs objects
     Args : a list of the matchs results """
    for match, result in zip(Match._registry[-len(results):], results):
        match.winner = result
    return


def adding_time_match(match_label_list):
    """ Adding the start_time and the end_time to the match object
    Arg : a list of start_time/end_time """

    for match in Match._registry[-len(match_label_list):]:
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
            player_object.winloss_ratio = round(player_object.num_of_wins / player_object.num_of_losses, 2)
        except ZeroDivisionError:
            if player_object.num_of_wins > 0:
                player_object.winloss_ratio = player_object.num_of_wins
            else:
                player_object.winloss_ratio = 0
        player_object.update_player_datas()

    return


def updating_general_rank_by_ratio():
    """ Use the player registry in order to reorganize the player's rank
    the 1st player is the one with the best ratio """

    players_dict = {}

    for player, index in zip(Player._registry, range(1, len(Player._registry) + 1)):
        players_dict[index] = [player.reference, player.ranking, player.winloss_ratio]

    sorted_by_wins = dict(sorted(players_dict.items(), key=lambda item: item[1][2], reverse=True))

    for player, rank in zip(sorted_by_wins, range(1, len(Player._registry)+1)):
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
    adding_result_match(results)
    adding_time_match(time_informations)
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
        adding_result_match(results)
        adding_time_match(time_informations)
        tournament_object.updating_scoreboard_score(number_of_round)
        tournament_object.sort_score_rank()
        show_score(sorted(tournament_object.scoreboard.values(), key=lambda k: k['score'],
                          reverse=True), number_of_round)

    tournament_object.serialized_the_object()
    updating_players_stats(tournament_object)
    updating_general_rank_by_ratio()
    tournament_object.serialized_the_object()

    return


def delete_tournament():
    """ Remove a selected tournament from the database """

    tournament_to_delete = view_tournament_manager.show_tournament_list(make_tournament_dict())
    database = TinyDB('database.json', indent=1)
    tournament_table = database.table("Tournament")

    tournament_table.remove(Query().name == tournament_to_delete)

    for value in Tournament._serialized_registry:
        if value['name'] == tournament_to_delete:
            Tournament._serialized_registry.remove(value)
    for tournament in Tournament._registry:
        if tournament.name == tournament_to_delete:
            Tournament._registry.remove(tournament)
    return

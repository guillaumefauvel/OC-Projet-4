
from models.player import Player
from models.tournament import Tournament
from datetime import datetime
import views.view_reports_manager as vrm
from controllers.controller_tournament_manager import updating_general_rank_by_ratio, player_researcher
import controllers.controller_menu

def reports_manager():
    """ Show the user the possibilities and gathered his answer.
    He is redirected in order to fulfill is choice."""

    answer = int(vrm.ask_for_report_choice())

    if answer == 1:
        vrm.show_list(make_players_dict())
        controllers.controller_menu.navigator(3)

    elif answer == 2:
        vrm.show_list(sort_by_rank())
        controllers.controller_menu.navigator(3)

    elif answer == 3:
        tournament_players_by_alpha()
        controllers.controller_menu.navigator(3)

    elif answer == 4:
        tournament_players_by_rank()
        controllers.controller_menu.navigator(3)

    elif answer == 5:
        vrm.show_tournaments_infos(make_tournament_dict())
        controllers.controller_menu.navigator(3)

    elif answer == 6:
        tournament_scoreboard()
        controllers.controller_menu.navigator(3)

    elif answer == 7:
        tournament_history()
        controllers.controller_menu.navigator(3)
    elif answer == 8:
        general_scoreboard()
        controllers.controller_menu.navigator(3)

    return


def make_players_dict():
    """ Make a player dictionnary by using the Player registry
    Return : A dictionnary with key = index, value_1 = player_reference,
    value_2 = player_ranking, value_3 = player_birthday"""
    players_dict = {}

    sorted_registry = sorted(Player._registry, key=lambda x: x.reference, reverse=False)

    for player, index in zip(sorted_registry, range(1, len(Player._registry)+1)):
        players_dict[index] = [player.reference, player.ranking, player.birthday]

    return players_dict


def make_tournament_dict():
    """ Create a tournament dictionnary by using the Tournament registry"""

    tournament_dict = {}

    for index, tournament in zip(range(1, len(Tournament._registry)+1), Tournament._registry):
        tournament_dict[index] = tournament.name, tournament.selected_players, \
                                 tournament.serialized_object, tournament.scoreboard, \
                                 tournament.location, tournament.start_date, \
                                 tournament.end_date, tournament.num_of_round

    return tournament_dict


def sort_by_rank():
    """ Use the player dict in order to etablish new rank
    Return : Another dict with a coherent indexes """
    updating_general_rank_by_ratio()
    sorted_by_rank = dict(sorted(make_players_dict().items(), key=lambda item: item[1][1]))
    fully_sorted = {}

    for value, new_index in zip(sorted_by_rank, range(1, len(sorted_by_rank)+1)):
        fully_sorted[new_index] = sorted_by_rank[value]

    return fully_sorted


def sort_by_age():
    """ Use the birthday infos in the player dict in order to sort the player
    by their age.
    Return : A sorted dict with the name and the age of the player"""

    age_dict = {}

    for value in make_players_dict():
        raw_date = make_players_dict()[value][2]
        birthday = datetime.strptime(raw_date, '%d/%m/%Y').date()
        num_of_days = datetime.now().date() - birthday
        age_dict[value] = make_players_dict()[value][0], round(num_of_days.days/365)

    sorted_by_age = dict(sorted(age_dict.items(), key=lambda item: item[1][1]))

    return sorted_by_age


def tournament_players_by_alpha():
    """ Sort alphabetically and return to the user the list of all
    the player of a given tournament """

    vrm.show_list(make_tournament_dict())
    tournament_choice = vrm.ask_tournament_choice(make_tournament_dict())
    vrm.show_tournament_players_by_alpha(make_tournament_dict()[tournament_choice])


def tournament_players_by_rank():
    """ Sort the player of a given tournament by rank and return them to the user
    by specifying their rank in the general scoreboard"""

    updating_general_rank_by_ratio()

    vrm.show_list(make_tournament_dict())
    tournament_choice = vrm.ask_tournament_choice(make_tournament_dict())
    players_list = make_tournament_dict()[tournament_choice][1]
    player_object = []
    for value in players_list:
        player_object.append(player_researcher(value)[0])
    player_dict = {}
    for value in player_object:
        player_dict[value.reference] = value.ranking
    player_dict = dict(sorted(player_dict.items(), key=lambda item: item[1]))
    vrm.show_tournament_players_by_rank(player_dict)


def tournament_scoreboard():
    """ Show the final scorebaord of the selected tournament """

    vrm.show_list(make_tournament_dict())
    tournament_choice = vrm.ask_tournament_choice(make_tournament_dict())
    tournament_name = make_tournament_dict()[tournament_choice][0]
    scoreboard = make_tournament_dict()[tournament_choice][3]
    vrm.show_scoreboard(sorted(scoreboard.values(), key=lambda k: k['score'], reverse=True), tournament_name)


def tournament_history_auxiliary(scoreboard, searched_reference, value_to_assign, results_indication):
    """ Auxiliary function used by tournament_history() in order to modify the scoreboard """

    for player in scoreboard:
        if scoreboard[player]['reference'] == searched_reference:
            scoreboard[player]['score'] += value_to_assign
            scoreboard[player]['round_result'] = results_indication
    return


def tournament_history():
    """ Show to the user the details of a selected tournament """

    vrm.show_list(make_tournament_dict())
    tournament_choice = vrm.ask_tournament_choice(make_tournament_dict())
    round_list = make_tournament_dict()[tournament_choice][2]
    players_list = make_tournament_dict()[tournament_choice][1]
    scoreboard = {}

    for player, index in zip(players_list, range(1, len(players_list)+1)):
        scoreboard[index] = {"reference": player, "score": 0, "rank": index, "round_result": ""}

    for round in round_list:
        for duel, result in zip(round_list[round][0], round_list[round][1]):
            player_1 = duel[0]
            player_2 = duel[1]
            if result == "1":
                tournament_history_auxiliary(scoreboard, player_1, 1, "G")
                tournament_history_auxiliary(scoreboard, player_2, 0, "-")
            elif result == "2":
                tournament_history_auxiliary(scoreboard, player_2, 1, "G")
                tournament_history_auxiliary(scoreboard, player_1, 0, "-")
            else:
                tournament_history_auxiliary(scoreboard, player_1, 0.5, "E")
                tournament_history_auxiliary(scoreboard, player_2, 0.5, "E")

        sorted_version = sorted(scoreboard.values(), key=lambda k: k['score'], reverse=True)

        for player, new_rank in zip(sorted_version, range(1, len(sorted_version)+1)):
            player['rank'] = new_rank

        vrm.show_duel(round_list[round][0])
        vrm.show_scoreboard_with_round(sorted_version, round)

    return


def general_scoreboard():
    """ Show the general scoreboard, it is sorted by ranking and it
    filters out every players that never played """

    sorted_list = sorted(Player._serialized_registry, key=lambda d: d['ranking'])
    filtered_list = [d for d in sorted_list if d['num_of_match'] > 0]
    vrm.show_general_scoreboard(filtered_list)

    return

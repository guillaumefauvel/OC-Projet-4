from models.player import Player
from models.match import Match
from models.tournament import Tournament
from models.round import Round

import views.view_tournament as vt
import views.view_tournament_manager as vtm
from views import view_menu

import controllers.controller_reports_manager as crm
import controllers.controller_menu as cm

from datetime import datetime


def tournament_manager():
    """ Show the user the possibilities and gathered his answer.
    He is redirected in order to fulfill is choice."""

    view_menu.view_header(13)
    answer = vtm.ask_choice()

    if answer is None:

        return cm.navigator(0, 3)

    if answer == "1":

        view_menu.view_header(14)
        tournament_launching()

    elif answer == "2":

        if len(unfinished_tournaments()) != 0:
            view_menu.view_header(1)
            selected_tournament = vtm.show_tournament_list(unfinished_tournaments(), 2)
            if selected_tournament is None:
                return cm.navigator(1, 2)
            name, finished_round, tournament_object, round_left = selected_tournament
            tournament_continuation(tournament_object, finished_round)
        else:
            tournament_manager()

    elif answer == "3":

        view_menu.view_header(2)
        delete_tournament()

    return


def tournament_launching():
    """ Create and launch a new tournament """

    player_dict = crm.make_players_dict()
    name, location, start_date, end_date, num_of_round, selected_players, game_type, notes \
        = vtm.new_tournament(player_dict)

    selected_players = [x[0] for x in selected_players]
    Tournament(name, location, start_date, end_date, num_of_round, selected_players, game_type, notes)

    last_tournament = (Tournament._registry[-1])
    launch_from_controller(last_tournament)

    return


def delete_tournament():
    """ Remove a selected tournament from the database """

    try:
        tournament_to_delete = vtm.show_tournament_list(crm.make_tournament_dict(), 1)[0]
    except TypeError:
        return cm.navigator(1, 2)

    for value in Tournament._serialized_registry:
        if value['name'] == tournament_to_delete:
            Tournament._serialized_registry.remove(value)
    for tournament in Tournament._registry:
        if tournament.name == tournament_to_delete:
            Tournament._registry.remove(tournament)

    cm.menu_loop(delete_tournament)

    return


def unfinished_tournaments():
    """ Return a dict of all the unfinished_tournament
    Return : A dict with key=index and value1=tournament_name,
    value2=int of round finished, value3=tournament=object,
    value4=round_left"""
    tournament_dict = {}
    index = 0
    for tournament in Tournament._registry:
        if tournament.num_of_round != len(tournament.serialized_object):
            index = index + 1
            round_left = tournament.num_of_round - len(tournament.serialized_object)
            tournament_dict[index] = tournament.name, len(tournament.serialized_object), tournament, round_left

    return tournament_dict


def tournament_status_treatment(booleans):
    """ Stop a tournament if the day has ended """

    if booleans is False:
        return True
    elif booleans is True:
        cm.menu_attribution(view_menu.menu_proposition())
        return False


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
        num_of_match = player_object.num_of_wins + player_object.num_of_losses + player_object.num_of_draw
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

    sorted_by_ratio = dict(sorted(players_dict.items(), key=lambda item: item[1][2], reverse=True))

    for player, rank in zip(sorted_by_ratio, range(1, len(Player._registry)+1)):
        player_researcher(sorted_by_ratio[player][0])[0].ranking = rank

    return


def launch_from_controller(tournament_object):
    """ Hold the logic behind a tournament
    Arg : A tournament object """

    tournament_object.return_ranking()
    list_of_duel = tournament_object.first_draw()
    vt.show_duel(list_of_duel)
    time_informations = vt.asking_end_match(list_of_duel)
    Round._registry[-1].end_time = datetime.now()
    results = vt.asking_match_result(list_of_duel)
    adding_result_match(results)
    adding_time_match(time_informations)
    tournament_object.updating_scoreboard_score(1)
    tournament_object.sort_score_rank()
    vt.show_score(sorted(tournament_object.scoreboard.values(),
                         key=lambda k: k['score'], reverse=True), 1)
    if not tournament_status_treatment(vt.asking_end_of_day()):
        return

    tournament_continuation(tournament_object, 1)

    return


def tournament_continuation(tournament_object, finished_round):
    """ Hold the mechanic behind the continuation of a tournament """
    # Iterate on the number of round left

    for number_of_round in range(finished_round+1, tournament_object.num_of_round + 1):
        # Generate the next series of duel thanks to the scoreboard
        list_of_duel = tournament_object.generating_other_draw(number_of_round)
        tournament_object.updating_scoreboard_associations(list_of_duel)
        vt.show_duel(list_of_duel)
        time_informations = vt.asking_end_match(list_of_duel)
        Round._registry[-1].end_time = datetime.now()
        results = vt.asking_match_result(list_of_duel)
        adding_result_match(results)
        adding_time_match(time_informations)
        tournament_object.updating_scoreboard_score(number_of_round)
        tournament_object.sort_score_rank()
        vt.show_score(sorted(tournament_object.scoreboard.values(), key=lambda k: k['score'],
                             reverse=True), number_of_round)

        tournament_object.serialized_the_object()
        if len(tournament_object.serialized_object) != tournament_object.num_of_round:
            if not tournament_status_treatment(vt.asking_end_of_day()):
                return

    updating_players_stats(tournament_object)
    updating_general_rank_by_ratio()
    view_menu.view_header(16)
    cm.launch_the_menu()

    return

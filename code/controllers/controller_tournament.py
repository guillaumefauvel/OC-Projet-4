from code.models.player import Player
from code.models.match import Match
from code.views.view_tournament import show_duel, asking_match_result, show_scoreboard, show_score

def make_player_dict():
    """Explore all the player object.
    Return a dictionnary : key=index, value=player_object """
    reference_dict = {}
    for index, player in zip(range(1, len(Player._registry)+1), Player._registry):
        reference_dict[index] = player

    return reference_dict

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


def launch_from_controller(tournament_object):
    NUM_OF_MATCH = int(len(tournament_object.selected_players)/2)
    # Sort the player by making an ordered dict
    tournament_object.return_ranking()
    # Use the ordered dict in order to create the scoreboard
    tournament_object.scoreboard_maker()
    tournament_object.scoreboard.purge()  # -DEVonly
    tournament_object.scoreboard_maker()  # -DEVonly
    # Generate the first series of duel thanks to the scoreboard
    list_of_duel = tournament_object.first_draw()
    # Show the user the list of duels
    show_duel(list_of_duel)
    # Ask the user the result of the match
    results = asking_match_result(list_of_duel)
    # Add those result to the match object
    adding_result_match(results, NUM_OF_MATCH)
    # Use these matchs objects to update the scoreboard
    tournament_object.updating_scoreboard_score(1)
    # Sort the scoreboard
    tournament_object.sort_score_rank()
    # show_scoreboard(tournament_object)
    # Show the scoreboard ( a copy version where it's fully sorted )
    show_score(sorted(tournament_object.scoreboard, key=lambda k: k['Score'], reverse=True), 1)

    # Iterate on the number of round left
    for number_of_round in range(2,tournament_object.num_of_round+1):
        # Generate the next series of duel thanks to the scoreboard
        list_of_duel = tournament_object.generator(number_of_round)
        tournament_object.updating_scoreboard_associations(list_of_duel)
        # show_scoreboard(tournament_object)
        show_duel(list_of_duel)
        results = asking_match_result(list_of_duel)
        adding_result_match(results, NUM_OF_MATCH)
        tournament_object.updating_scoreboard_score(number_of_round)
        tournament_object.sort_score_rank()
        # show_scoreboard(tournament_object)
        show_score(sorted(tournament_object.scoreboard, key=lambda k: k['Score'],reverse=True),number_of_round)


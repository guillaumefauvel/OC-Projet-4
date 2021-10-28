from code.models.player import Player
from code.models.match import Match
from code.views.view_tournament import show_duel, asking_match_result

def make_player_dict():
    """Explore all the player object.
    Return a dictionnary : key=index, value=player_object """
    reference_dict = {}
    for index, player in zip(range(1, len(Player._registry)), Player._registry):
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

    for line in tournament_object.scoreboard:
        print(line)
    # Generate the next series of duel thanks to the scoreboard

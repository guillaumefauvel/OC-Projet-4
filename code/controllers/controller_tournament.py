from code.models.player import Player
from code.views.view_tournament import show_duel


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
                print("found")
    return researched_results

def launch_from_controller(tournament_object):
    # Sort the player by making an ordered dict
    tournament_object.return_ranking()
    # Use the ordered dict in order to create the scoreboard
    tournament_object.scoreboard_maker()
    tournament_object.scoreboard.purge()  # -DEVonly
    tournament_object.scoreboard_maker()  # -DEVonly
    # Generate the first series of duel thanks to the scoreboard
    # Show the user the list of duels
    show_duel(tournament_object.first_draw())
    # Ask the user the result of the match



    # Generate the next series of duel thanks to the scoreboard
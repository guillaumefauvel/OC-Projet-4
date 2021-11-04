from controllers import controller_tournament
from models.tournament import Tournament
from views import view_menu, view_new_tournament, view_players_manager
from controllers.controller_tournament import launch_from_controller, convert_to_reference
from controllers.controller_reports_manager import reports_manager
from controllers.controller_players_manager import players_manager

def menu_attribution(response):
    # Launch a new tournament
    if response == 1:
        tournament_launching()
    # Go to the player manager
    elif response == 2:
        players_manager()
        pass
    # Generate a report
    elif response == 3:
        reports_manager()
        pass
    # Quit the program
    elif response == 4:
        pass


def tournament_launching():
    """ Create and launch a new tournament """

    # Make a dict of all the listed player
    player_dict = controller_tournament.make_player_dict()
    # Give that dict as an argument for the user view and gather the tournaments informations
    name, location, start_date, end_date, num_of_round, selected_players, game_type, notes \
        = view_new_tournament.new_tournament(player_dict)
    # Create the tournament
    selected_players = convert_to_reference(selected_players)
    Tournament(name, location, start_date, end_date, num_of_round, selected_players, game_type, notes)
    # Launch the tournament
    last_tournament = (Tournament._registry[-1])
    launch_from_controller(last_tournament)
    return

def tournament_beta_purposes():
    last_tournament = (Tournament._registry[-1])
    last_tournament.launch()
    pass

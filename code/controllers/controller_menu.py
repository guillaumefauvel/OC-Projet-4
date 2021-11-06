
from controllers.controller_tournament_manager import launch_from_controller, convert_to_reference, make_player_dict, tournament_manager
from controllers.controller_reports_manager import reports_manager
from controllers.controller_players_manager import players_manager

def menu_attribution(response):
    # Launch a new tournament
    if response == 1:
        tournament_manager()
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



from code.controllers import controller_tournament
from code.models.tournament import Tournament
from code.models.player import Player
from code.views import view_menu, view_new_tournament, view_player_form

def menu_attribution(response):
    # Launch a new tournament
    if response == 1:
        tournament_beta_purposes()

    # add a new player
    elif response == 2:
        adding_player()

    # save the system state
    elif response == 3:
        pass

    # load a save
    elif response == 4:
        pass

    # generate a report
    elif response == 5:
        pass

    # consult player infos
    elif response == 6:
        pass

    # quit the program without saving
    elif response == 7:
        pass


def tournament_launching():
    """ Create and launch a new tournament """

    # Make a dict of all the listed player
    player_dict = controller_tournament.make_player_dict()
    # Give that dict as an argument for the user view and gather the tournaments informations
    name, location, start_date, end_date, num_of_round, selected_players, game_type, notes \
        = view_new_tournament.new_tournament(player_dict)
    # Create the tournament
    Tournament(name, location, start_date, end_date, num_of_round, selected_players, game_type, notes)
    # Launch the tournament
    last_tournament = (Tournament._registry[-1])
    last_tournament.launch()
    return

def adding_player():
    """ Create a new player object from the gathered informations
    If the user doesn't select menu return he can continue his players creations"""

    name, first_name, birthday, gender, ranking = view_player_form.new_player()
    Player(name, first_name, birthday, gender, ranking)
    if view_menu.ask_menu_return() == True:
        menu_attribution(view_menu.menu_proposition())
    return adding_player()

def tournament_beta_purposes():
    last_tournament = (Tournament._registry[-1])
    last_tournament.launch()
    pass

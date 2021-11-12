
from models.player import Player
from controllers.controller_reports_manager import make_players_dict
import controllers.controller_menu as cm
import views.view_players_manager as vpm
import views.view_reports_manager as vrm
import views.view_menu as vm


def players_manager():
    """ Show the user the possibilities and gathered his answer.
    He is redirected in order to fulfill is choice."""

    vm.view_header(12)

    answer = vpm.ask_choice()

    if answer == "":
        return cm.navigator(0, 3)

    if answer == "1":
        vm.view_header(10)
        adding_player()

    elif answer == "2":
        vm.view_header(3)
        delete_player()

    elif answer == "3":
        vm.view_header(4)
        player_informations()

def adding_player():
    """ Create a new player object from the gathered informations"""

    name, first_name, birthday, gender, ranking = vpm.new_player()
    Player(name, first_name, birthday, gender, ranking)

    cm.menu_loop(adding_player)


def delete_player():
    """ Remove a player from the database """

    vrm.show_list_of_players(make_players_dict())
    player_to_delete = vpm.ask_player_selection(make_players_dict())

    if player_to_delete == None:
        return cm.navigator(2,2)

    for value in Player._serialized_registry:
        if value['reference'] == player_to_delete:
            Player._serialized_registry.remove(value)
    for player in Player._registry:
        if player.reference == player_to_delete:
            player._registry.remove(player)

    cm.menu_loop(delete_player)

    return


def player_informations():
    """ Show the informations of a player """

    vrm.show_list_of_players(make_players_dict())
    selected_player = vpm.ask_player_selection(make_players_dict())
    if selected_player == None:
        return cm.navigator(2,2)

    for player in Player._serialized_registry:
        if player['reference'] == selected_player:
            player_infos = player
            vpm.show_player_infos(player_infos)

    cm.menu_loop(player_informations)

    return


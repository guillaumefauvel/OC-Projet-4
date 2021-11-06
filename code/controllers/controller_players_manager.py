from models.player import Player
from views import view_menu, view_tournament_manager, view_players_manager, view_reports_manager
from controllers.controller_reports_manager import make_players_dict
from controllers.controller_tournament_manager import updating_general_rank_by_ratio, player_researcher

from tinydb import TinyDB, Query

def players_manager():
    answer = view_players_manager.ask_choice()
    if answer == "1":
        adding_player()

    elif answer == "2":

        delete_player()

    elif answer == "3":

        show_player_infos()

def adding_player():
    """ Create a new player object from the gathered informations"""
    name, first_name, birthday, gender, ranking = view_players_manager.new_player()
    Player(name, first_name, birthday, gender, ranking)

def delete_player():
    """ Remove a player from the database """

    player_to_delete = view_players_manager.show_player_list(make_players_dict())
    database = TinyDB('database.json', indent=1)
    player_table = database.table("Player")

    player_table.remove(Query().reference == player_to_delete)
    for value in Player._serialized_registry:
        if value['reference'] == player_to_delete:
            Player._serialized_registry.remove(value)
    for player in Player._registry:
        if player.reference == player_to_delete:
            player._registry.remove(player)

    return

def show_player_infos():
    """ Show the informations of a player """

    selected_player = view_players_manager.show_player_list(make_players_dict())

    for player in Player._serialized_registry:
        if player['reference'] == selected_player:
            player_infos = player
    view_players_manager.show_player_infos(player_infos)

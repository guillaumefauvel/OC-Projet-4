""" Report Manager - View """
from prettytable import PrettyTable
import math

def ask_for_report_choice():
    """ Show the possible reports and ask the user his selection
    Return : An int that correspond to the user choice"""

    print("Quel type de rapport voulez-vous générer ? \n")
    print("  1. Une liste de tous les joueurs classée par ordre alphabétique")
    print("  2. Une liste de tous les joueurs classée par classement")
    print("  3. Une liste de tous les joueurs d'un tournoi classée par ordre alphabétique")
    print("  4. Une liste de tous les joueurs d'un tournoi classée par classement")
    print("  5. Une liste de tous les tournois")
    print("  6. Le tableau des scores d'un tournoi")
    print("  7. Le récapitulatif d'un tournoi")
    print("  8. Le tableau des scores")

    possible_choice = ["","1", "2", "3", "4", "5", "6", "7", "8"]

    while True:
        answer = input("\nRéponse : ")
        if answer in possible_choice:
            break
        else:
            print("->Merci de rentrer un index correct")

    return answer


def show_list(dictionnary):
    """ Show the key and the value of a dictionnary
    Arg : A dictionnary """
    print("")
    for value in dictionnary:
        print(f"{value}. {dictionnary[value][0]}")

    return


def ask_tournament_choice(dictionnary):
    """ Ask for the key of a dictionnary
    Arg : A dictionnary with index key
    Return : The selected key ( an int )"""
    while True:
        answer = input("\nQuel tournois désirer vous consulter ? ")
        try:
            test = dictionnary[int(answer)]
            break
        except KeyError:
            print("Merci d'indiquer un index valide")
        except ValueError:
            print("Merci d'indiquer un index valide")

    return int(answer)


def show_tournament_players_by_alpha(selected_tournament):
    """ Show every player of a tournament by their alphabetical order
    Arg : The dictionnary of a tournament """
    print("")
    player_list = []
    for value in selected_tournament[1]:
        player_list.append(value)

    for index, player in zip(range(1, len(player_list)+1), sorted(player_list)):
        print(f"{index}. {player}")

    return


def show_tournament_players_by_rank(selected_tournament):
    """ Show every player of a tournament sorted by their rank
    Arg : The dictionnary of a tournament """
    print("")
    for player in selected_tournament:
        print(f"{selected_tournament[player]}. {player}")

    return


def show_tournaments_infos(tournament_dict):
    """ Show the informations of a tournament
    Arg : The dictionnary of a tournament """
    print("")
    for tournament in tournament_dict:
        name = tournament_dict[tournament][0]
        num_of_players = len(tournament_dict[tournament][1])
        location = tournament_dict[tournament][4]
        start_date = tournament_dict[tournament][5]
        end_date = tournament_dict[tournament][6]
        num_of_round = tournament_dict[tournament][7]
        print(f"Nom du tournoi : {name}")
        print(f"Lieu : {location}")
        print(f"Nombre de participants : {num_of_players}")
        print(f"Nombre de round : {num_of_round}")
        print(f"Date : {start_date} au {end_date}")
        print("\n                 ---\n")

    return


def show_scoreboard(scoreboard, tournament_name):
    """ Show the final scoreboard of a tournament
    Args : The scoreboard ( a dict ), the name of the tournament """
    table = PrettyTable(["Joueur", "Classement", "Score"])
    for value in scoreboard:
        table.add_row([value["reference"], value["scorerank"], value["score"]])
    table = table.get_string(title=f"{tournament_name}")

    print(table)

    return


def show_scoreboard_with_round(scoreboard, round_number):
    """ Show the scoreboard of a tournament at the end of a round
    Args : The scoreboard ( a dict ), the round number """
    table = PrettyTable(["Joueur", "Classement", "Score", "Résulat-Round"])
    for value in scoreboard:
        table.add_row([value["reference"], value["rank"],
                       value["score"], value['round_result']])
    table = table.get_string(title=f"Round N°{round_number}")

    print(table)

    return


def show_general_scoreboard(scoreboard):
    """ Show the general scoreboard
    Arg : A scoreboard ( dict ) """
    table = PrettyTable(["Joueur", "Classement", "RatioG/P", "Matchs joués",
                         "Matchs gagnés", "Matchs perdus", "Egalité", "Tournois joués"])
    for value in scoreboard:
        table.add_row([value["reference"], value["ranking"], value["win_loss_ratio"],
                       value["num_of_match"], value["num_of_wins"], value["num_of_losses"],
                       value["num_of_draw"], value["num_of_tournaments"]])
    table = table.get_string(title=f"-Tableau des scores-")

    print(table)

    return


def show_duel(list_of_duel):
    """ Show a formated list of duel
    Arg : A list of duel ( a duel is a list of 2 player references ) """
    print("")
    for duel in list_of_duel:
        print(f"{duel[0]} affrontais {duel[1]}")
    print("")

    return

def show_list_of_players(player_dict):
    """ Show a list of player in a compact way
    Arg : A player dict """
    new_dict = {}
    table = PrettyTable(["C1","C2","C3"])
    div = len(player_dict)//3
    remainder = len(player_dict)%3

    for value in range(1,div+1):
        first_player = f"{value}. {player_dict[value][0]}"
        second_player = f"{value+div}. {player_dict[value+div][0]}"
        third_player = f"{value+div*2}. {player_dict[value+div*2][0]}"
        # new_dict[value] = [player_dict()[value][0], player_dict()[value+div][0], player_dict()[value+div*2][0]]
        new_dict[value] = [first_player, second_player, third_player]
    if remainder == 1:
        first_player = f"{len(player_dict)}. {player_dict[len(player_dict)][0]}"
        new_dict[div+1] = [first_player,"",""]
    else:
        first_player = f"{len(player_dict)-1}. {player_dict[len(player_dict-1)][0]}"
        second_player = f"{len(player_dict)}. {player_dict[len(player_dict)][0]}"
        new_dict[div+1] = [first_player,second_player,""]

    for value in new_dict:
        table.add_row(new_dict[value])

    print(table)

    return

def show_tournament_name(tournament_name):
    """ Show a formated version of the tournament name
    Arg : a string containing the tournament name """

    layer = f"+{'-'*64}+"
    name_lenght = int(len(tournament_name)/2)
    new_form = f"|{(int(63/2)-name_lenght)*' '}{tournament_name}{((int(63/2)-name_lenght+1))*' '}|"
    print(layer)
    print(new_form)
    print(layer)

    return

""" Report Manager - View """
from prettytable import PrettyTable


def ask_for_report_choice():
    print("\n----- GESTION DES RAPPORTS -----")
    print("\nQuel type de rapport voulez-vous générer ? \n")
    print("  1. Une liste de tous les joueurs classée par ordre alphabétique")
    print("  2. Une liste de tous les joueurs classée par classement")
    print("  3. Une liste de tous les joueurs d'un tournoi classée par ordre alphabétique")
    print("  4. Une liste de tous les joueurs d'un tournoi classée par classement")
    print("  5. Le tableau des scores d'un tournoi")
    print("  6. Une liste de tous les tournois")
    print("  7. Une liste de tous les tours d'un tournoi")
    print("  8. Une liste de tous les matchs d'un tournoi")

    possible_choice = ["1","2","3","4","5","6","7"]

    while True:
        answer = input("\nRéponse : ")
        if answer in possible_choice:
            break
        else:
            print("->Merci de rentrer un index correct")

    return answer

def show_list(dict):
    print("")
    for value in dict:
        print(f"{value}. {dict[value][0]}")

    return

def ask_tournament_choice(dict):
    while True:
        answer = input("\nQuel tournois désirer vous consulter ? ")
        try:
            test = dict[int(answer)]
            break
        except:
            print("Merci d'indiquer un index valide")

    return int(answer)

def show_tournament_players_by_alpha(selected_tournament):

    print("")
    player_list = []
    for value in selected_tournament[1]:
        player_list.append(value)

    for index, player in zip(range(1,len(player_list)+1),sorted(player_list)):
        print(f"{index}. {player}")

    return

def show_tournament_players_by_rank(selected_tournament):

    print("")
    for player in selected_tournament:
        print(f"{selected_tournament[player]}. {player}")

    return

def show_tournaments_infos(tournament_dict):

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

    table = PrettyTable(["Joueur","Classement","Score"])
    for value in scoreboard:
        table.add_row([value["reference"], value["scorerank"], value["score"]])
    table = table.get_string(title=f"{tournament_name}")

    print(table)

    return
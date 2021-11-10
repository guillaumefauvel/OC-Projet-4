import views.view_reports_manager as vrm

def check_date(caraccteristic):
    """Check if the input date fit the asked format, if not it show an error and ask again"""
    while True:
        answer = input(caraccteristic)
        if len(answer) == 10 and answer[2] == "/" and answer[5] == "/":
            return answer
        else:
            print("---< Merci d'entrer une date au format 'JJ/MM/AAAA'. ")
    pass

def new_tournament(player_dict):
    """ Form that gather informations from the user in order to make a tournament
    Arg : A dictionnary of all the listed players
    Return : All the informations needed to create a tournament"""

    print("\n\n-------------------------------------")
    print("-- Lancement d'un nouveau tournoi. --")
    print("-------------------------------------\n")

    tournament_caracteristics = ["Nom : ", "Lieu : ", "Date de début (JJ/MM/AAAA): ", "Date de fin (JJ/MM/AAAA): ",
                                 "Nombre de tours : " , "\nJoueurs séléctionnés : ", "Type de jeu : " ,"Notes : " ]
    tournament_input = []

    for caraccteristic in tournament_caracteristics:
        if caraccteristic == "Date de début (JJ/MM/AAAA): ":

            tournament_input.append(check_date(caraccteristic))

        elif caraccteristic == "Date de fin (JJ/MM/AAAA): ":

            tournament_input.append(check_date(caraccteristic))

        elif caraccteristic == 'Nombre de tours : ':
            while True:
                answer = input(caraccteristic)
                try:
                    answer = int(answer)
                    if answer > 0:
                        tournament_input.append(answer)
                        break
                    else:
                        print("-> Merci d'indiquer un entier supérieur à 0")
                except ValueError:
                    print("-> Merci d'indiquer un entier supérieur à 0")
        elif caraccteristic == "\nJoueurs séléctionnés : ":
            print("")

            vrm.show_list_of_players(player_dict)

            selected_players = []

            while True:

                answer = input(caraccteristic)
                answer_list = answer.split()
                if len(answer_list)%2 != 0:
                    print("-> Merci de saisir un nombre pair")
                if len(answer_list) != len(set(answer_list)):
                    print("-> Merci de saisir un joueur une seul fois")
                elif len(answer_list)%2 == 0 and len(answer_list) == len(set(answer_list)):
                    try:
                        answer_list_conversion = [int(value) for value in answer_list]
                        verification = sum(answer_list_conversion)
                        for player in answer_list_conversion:
                            for index in player_dict:
                                if player == index:
                                    selected_players.append(player_dict[index])
                        tournament_input.append(selected_players)
                        break
                    except TypeError:
                        print('-> Merci de rentrer des index valides')
                    except ValueError:
                        print('-> Merci de rentrer des index valides')

        elif caraccteristic == "Type de jeu : ":
            print("\n   1. Bullet ( 1 min/j ) \n   2. Blitz ( 5 min/j ) \n   3. Coup rapide ( 10 min/j ) \n")
            while True:
                response = input("Type de jeu : ")
                if response == "1":
                    game_type_choice = "Bullet"
                    tournament_input.append(game_type_choice)
                    break
                elif response == "2":
                    game_type_choice = "Blitz"
                    tournament_input.append(game_type_choice)
                    break
                elif response == "3":
                    game_type_choice = "Coup rapide"
                    tournament_input.append(game_type_choice)
                    break
                else:
                    print("\n-> Merci de répondre '1','2' ou '3' \n")
        else:
            answer = input(caraccteristic)
            tournament_input.append(answer)

    name, location, start_date, end_date, num_of_round, selected_players, game_type, notes = tournament_input

    return name, location, start_date, end_date, num_of_round, selected_players, game_type, notes


def ask_choice():
    """ Show the user his possible choices and ask him his selection """
    print("\n-------------------------------")
    print("---- GESTION DES TOURNOIS -----")
    print("-------------------------------")
    print("\nQue souhaitez faire ? \n\n  1. Lancer un nouveau tournoi \n  2."
          " Reprendre un tournoi en cours \n  3. Supprimer un tournoi")
    while True:
        answer = input("\nRéponse : ")
        if answer in ["1","2","3"]:
            break
        else:
            print("->Merci de rentrer 1, 2 ou 3.")
    return answer

def show_tournament_list(dict,mode):
    """ Show a list of tournament and ask the index of the selected tournament
    Arg : a tournament dict, a mode that use a variant of the origin function"""
    print("")
    if mode == 1:
        for value in dict:
            print(f"{value}. {dict[value][0]}")
    if mode == 2:
        for value in dict:
            print(f"{value}. {dict[value][0]} - [{dict[value][3]} round(s) restant(s)]")

    while True:
        try:
            selected_tournament = int(input("\nQuel tournoi voulez-vous sélectionner ? "))
            if selected_tournament in dict.keys():
                break
            else:
                print("->Merci de rentrer un index valide")
        except ValueError:
            print("->Merci de rentrer un index valide")

    selected_tournament = dict[selected_tournament]

    return selected_tournament

def no_unfinished_tournament():
    """ Indicate to the user that there is no unfinished tournament """
    print("-> Tout les tournois ont été terminé")
    return


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
    """ Form that gather informations from the user in order to make a tournament """

    print("\n -- Lancement d'un nouveau tournoi. \n")

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
            for player in player_dict:
                print(f"   {player}. {player_dict[player].reference}")
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

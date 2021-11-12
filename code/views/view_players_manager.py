from datetime import datetime


def ask_choice():
    """ Query the user choice
    Return : An int that correspond to the user choice """

    print("Que souhaitez faire ? \n\n  1. Ajouter un nouveau joueur\n  2."
          " Supprimer un joueur \n  3. Rechercher les informations d'un joueur")

    while True:
        answer = input("\nRéponse : ")
        if answer in ["", "1", "2", "3"]:
            break
        else:
            print("->Merci de rentrer 1,2 ou 3.")

    return answer


def new_player():
    """ Form that gather player informations
    Return : Informations that are needed to create a player object"""

    player_infos = []
    player_type = ["Nom : ", "Prénom : ", "Date de naissance : ", "Genre [H/F]: ", "Classement : "]
    for info in range(len(player_type)):

        if player_type[info] == "Date de naissance : ":
            while True:
                take = input(player_type[info])
                try:
                    datetime.strptime(take, "%d/%m/%Y")
                    player_infos.append(take)
                    break
                except ValueError:
                    print("---< Merci d'entrer une date au format 'JJ/MM/AAAA'. ")

        elif player_type[info] == "Genre [H/F]: ":
            while True:
                take = input(player_type[info])
                if take.lower() == "h" or take.lower() == "f":
                    player_infos.append(take.upper())
                    break
                else:
                    print("Merci d'entrer 'H' ou 'F' ")

        elif player_type[info] == "Classement : ":
            while True:
                take = input(player_type[info])
                try:
                    player_infos.append(int(take))
                    break
                except ValueError:
                    print("Merci de rentrer un entier")

        else:
            take = input(player_type[info])
            player_infos.append(take)

    name, first_name, birthday, gender, ranking = player_infos

    return name, first_name, birthday, gender, ranking


def ask_player_selection(player_dict):
    """ Show a list of players and ask the index of the selected players
    Arg : a player dict"""

    while True:
        try:
            selected_player = input("\nQuel joueur voulez-vous sélectionner ? ")
            if selected_player == "":
                return
            if int(selected_player) in player_dict.keys():
                break
            else:
                print("->Merci de rentrer un index valide")
        except ValueError:
            print("->Merci de rentrer un index valide")

    selected_player = player_dict[int(selected_player)][0]

    return selected_player


def show_player_infos(player_infos):
    """ Show the informations of a selected player
    Arg : The serialized infos of the selected player """
    print("")
    if player_infos['gender'] == "H":
        print(f"--- informations du joueur : {player_infos['reference']} ---\n")
    else:
        print(f"--- informations de la joueuse : {player_infos['reference']} ---\n")
    list_of_infos = ['Nom', 'Prénom', 'Date de naissance', 'Genre', 'Classement', '',
                     'Nombre de match gagnés', 'Nombre de match perdus',
                     'Nombre de match nuls', 'Ratio Victoires/Défaites', 'Nombre de match joués',
                     'Nombre de tournois joués', ]
    for infos_type, value in zip(list_of_infos, player_infos):
        if len(infos_type) > 2:
            print(f"{infos_type}: {player_infos[value]}")
        else:
            pass

    return

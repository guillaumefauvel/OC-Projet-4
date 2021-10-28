
def new_player():
    """ Form that gather player informations
    Return : Informations that are needed to create a player object"""

    print("\n -- Ajout d'un nouveau joueur. \n ")
    player_infos = []
    player_type = ["Nom : ", "Prénom : ", "Date de naissance : ", "Genre [H/F]: ", "Classement : "]
    for info in range(len(player_type)):

        if player_type[info] == "Date de naissance : ":
            while True:
                take = input(player_type[info])
                if len(take) == 10 and take[2] == "/" and take[5] == "/":
                    player_infos.append(take)
                    break
                else:
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
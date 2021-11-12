

def verify_menu_command():
    """ Check if the input is as expected """

    while True:
        response = input("\nVotre choix : ")
        try:
            response = int(response)
            if 7 > response > 0:
                return response
            else:
                print("Veuillez saisir un entier entre 1 et 6")
        except ValueError:
            print("Veuillez saisir un entier entre 1 et 6")


def menu_proposition():
    """ Show the user the menu possibilities and ask his choice
    Return : A int associated to the user anwser """
    view_header(15)

    print("Que voulez-vous faire ? \n\n  1. Gestion des tournois \n  2. Gestion des joueurs "
          "\n  3. Gestion des rapports \n  "
          "4. Sauvegarder l'état du programme \n  5. Quitter le programme en sauvegardant \n"
          "  6. Quitter le programme sans sauvegarder \n")
    response = verify_menu_command()

    return response


def ask_menu_return():
    """ An input function that ask the user if he want to go to the menu """

    while True:
        response = input("\nVoulez-vous revenir au menu ? 'Y/N' \n")
        if response.lower() == "y":
            return True
        elif response.lower() == "n":
            return False
        else:
            print("Merci de répondre par oui 'y' ou par non 'n'")

def view_header(header_ref):
    """ Show a header
    Arg : an int, the header reference """
    dict_of_header = {1:"-- Reprise d'un tournoi --",
                      2:"-- Suppression d'un tournoi --",
                      3:"-- Suppression d'un joueur --",
                      4:"-- Informations d'un joueur --",
                      5:"-- Joueurs classés par ordre alphabétique --",
                      6:"-- Joueurs classés par rang --",
                      7:"-- Liste de tout les tournois --",
                      8:"-- Tableau des scores d'un tournoi --",
                      9:"-- Récapitulatif d'un tournois --",
                      10:"-- Ajout d'un nouveau joueur --",
                      11:"----- GESTION DES RAPPORTS -----",
                      12:"----- GESTION DES JOEURS -----",
                      13:"----- GESTION DES TOURNOIS -----",
                      14:"-- Lancement d'un nouveau tournoi --",
                      15:"---------- MENU ----------",
                      16:"----- FIN DU TOURNOI -----"}

    print("\n"+len(dict_of_header[header_ref])*"-")
    print(dict_of_header[header_ref])
    print(len(dict_of_header[header_ref])*"-"+"\n")

    return

def confirm_quit():
    """ Ask the user the user if he is sure that he want to quit
    the program without saving
    Return : A boolean """
    while True:
        response = input("\nVoulez-vous vraiment quitter le programme sans sauvegarder ? y/n ")
        if response == "y":
            return True
        elif response == "n":
            return False
        else:
            print("->Merci de répondre par oui (y) ou par non (n).")
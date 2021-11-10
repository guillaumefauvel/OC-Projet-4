

def verify_menu_command():
    """ Check if the input is as expected """

    while True:
        response = input("\nVotre choix : ")
        try:
            response = int(response)
            if 5 > response > 0:
                return response
            else:
                print("Veuillez saisir un entier entre 1 et 4")
        except ValueError:
            print("Veuillez saisir un entier entre 1 et 4")


def menu_proposition():
    """ Show the user the menu possibilities and ask his choice
    Return : A int associated to the user anwser """

    print("\nQue voulez-vous faire ? \n\n  1. Gestion des tournois \n  2. Gestion des joueurs "
          "\n  3. Gestion des rapports \n  "
          "4. Quitter le programme")
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
                      9:"-- Récapitulatif d'un tournois --"}

    print("\n\n"+len(dict_of_header[header_ref])*"-")
    print(dict_of_header[header_ref])
    print(len(dict_of_header[header_ref])*"-")

    return



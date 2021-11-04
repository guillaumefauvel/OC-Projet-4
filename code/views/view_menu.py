
def verify_menu_command():
    """ Check if the input is as expected """

    while True:
        response = input("\nVotre choix : ")
        try:
            response = int(response)
            if response > 0 and response < 8:
                return response
            else:
                print("Veuillez saisir un entier entre 1 et 5")
        except ValueError:
            print("Veuillez saisir un entier entre 1 et 5")

def menu_proposition():
    """ The general menu logic """

    print("\nQue voulez-vous faire ? \n\n  1. Lancer un nouveau tournoi \n  2. Gestion des joueurs "
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
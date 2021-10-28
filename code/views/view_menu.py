
def verify_menu_command():
    """ Check if the input is as expected """

    while True:
        response = input("\nVotre choix : ")
        try:
            response = int(response)
            if response > 0 and response < 8:
                return response
            else:
                print("Veuillez saisir un entier entre 1 et 7")
        except ValueError:
            print("Veuillez saisir un entier entre 1 et 7")

def menu_proposition():
    """ The general menu logic """

    print("\nQue voulez-vous faire ? \n\n  1. Lancer un nouveau tournoi \n  2. Ajouter un nouveau joueur "
          "\n  3. Sauvegarder l'état du système \n  4. Charger une sauvegarde \n  5. Générer un rapport "
          "\n  6. Consulter les informations d'un joueur \n  7. Quitter le programme sans sauvegarder ")
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
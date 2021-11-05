""" Report Manager - View """

def ask_for_report_choice():
    print("\n----- GESTION DES RAPPORTS -----")
    print("\nQuel type de rapport voulez-vous générer ? \n")
    print("  1. Une liste de tous les joueurs classée par ordre alphabétique")
    print("  2. Une liste de tous les joueurs classée par classement")
    print("  3. Une liste de tous les joueurs d'un tournoi classée par ordre alphabétique")
    print("  4. Une liste de tous les joueurs d'un tournoi classée par classement")
    print("  5. Une liste de tous les tournois")
    print("  6. Une liste de tous les tours d'un tournoi")
    print("  7. Une liste de tous les matchs d'un tournoi")

    possible_choice = ["1","2","3","4","5","6","7"]

    while True:
        answer = input("\nRéponse : ")
        if answer in possible_choice:
            break
        else:
            print("->Merci de rentrer un index correct")

    return answer

def show_list(dict):

    for value in dict:
        print(f"{value}. {dict[value][0]}")

    return
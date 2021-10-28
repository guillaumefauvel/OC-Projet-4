""" View generated during the tournament """

def show_duel(list_of_duel):
    """ Print the list of duel """
    for player, index in zip(list_of_duel,range(len(list_of_duel))):
        print(f"{index+1}.{player[0]} affrontera {player[1]}.\n")


def asking_match_result(duel):
    """ Ask the user wich of the player win.
    Attrs:
    - duel : the list of two players
    Returns:
    - A list where '1' or '2' = the winner ref, None if there is an equality
    """
    result_list = []
    for player in duel:
        while True:
            accepted_answer = ["0","1","2"]
            print(f"1.{player[0]}, 2.{player[1]}\n"
                  f"Qui du joueur 1 ou du joueur 2 a gagné ? '0' si nul")
            winner = input("Réponse : ")
            if winner in accepted_answer:
                if winner == "0":
                    result_list.append(None)
                    break
                else:
                    result_list.append(winner)
                    break
            else:
                "Merci de rentrer '1','2' ou '0'."

    return result_list
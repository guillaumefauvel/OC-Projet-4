""" View generated during the tournament """
from prettytable import PrettyTable

def show_duel(list_of_duel):
    """ Print the list of duel """
    for player, index in zip(list_of_duel,range(len(list_of_duel))):
        print(f"\n{index+1}.{player[0]} affrontera {player[1]}.")

    print('\n--------------------------------------------------------')


def asking_match_result(duel):
    """ Ask the user wich of the player win.
    Arg :
    - duel : the list of two players
    Return :
    - A list where '1' or '2' equals the winner ref, None if there is an equality
    """
    result_list = []
    for player in duel:
        while True:
            accepted_answer = ["0","1","2"]
            print(f"\n1.{player[0]}, 2.{player[1]}\n"
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

    print('--------------------------------------------------------')

    return result_list

# -DEVonly
def show_scoreboard(tournament_object):

    print('--------------------------------------------------------')

    for value in sorted(tournament_object.scoreboard, key=lambda k: k['Score'],reverse=True):
        print(value)

    print('--------------------------------------------------------')

def show_score(scoreboard,round_number):

    table = PrettyTable(["Joueur","Classement","Score"])
    for value in scoreboard:
        table.add_row([value["Reference"], value["ClassementScore"], value["Score"]])
    table = table.get_string(title=f"Round {round_number}")
    print(table)



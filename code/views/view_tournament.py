""" View generated during the tournament """
from prettytable import PrettyTable
import datetime


def show_duel(list_of_duel):
    """ Print the list of duel """
    print('\n--------------------------------------------------------')

    for player, index in zip(list_of_duel, range(len(list_of_duel))):
        print(f"\n{index+1}.{player[0]} affrontera {player[1]}.")

    print('\n--------------------------------------------------------')


def asking_end_match(duel_list):
    """ Ask the user wich match has ended in
    order to track the end time of a match
    Args : The list of the duel
    Return : A dict containing each match,
    the start_time and the end_time (dt_object)
    """
    start_time = datetime.datetime.now()
    match_dict = {}
    short_term_dict = {}

    for match, index in zip(duel_list, range(1, len(duel_list)+1)):
        print(f"{index}. {match[0]} contre {match[1]}")
        match_dict[index] = {'match': match}, {'start_time': start_time}
        short_term_dict[index] = ""
    print("\nUn match viens de se terminer ? Merci d'entrer son numéro")

    for value in range(len(duel_list)):
        while True:
            try:
                answer = int(input("\nNuméro du match : "))
                short_term_dict.pop(answer)
                match_dict[answer] = match_dict[answer], datetime.datetime.now()
                break
            except ValueError:
                print("\nMerci d'entrer un index correct")
            except KeyError:
                print("\nMerci de rentrer un index encore présent dans la liste :\n")
                print(''.join(['{0}.  {1}'.format(k, v) for k, v in short_term_dict.items()]))
    return match_dict


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
            accepted_answer = ["0", "1", "2"]
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


def show_scoreboard(tournament_object):
    """ DEVonly """

    print('--------------------------------------------------------')

    for value in sorted(tournament_object.scoreboard.values(), key=lambda k: k['score'], reverse=True):
        print(value)

    print('--------------------------------------------------------')


def show_score(scoreboard, round_number):
    """ Show the scoreboard
    Args : A scoreboard ( which is a dict ), a round number"""

    table = PrettyTable(["Joueur", "Classement", "Score"])
    for value in scoreboard:
        table.add_row([value["reference"], value["scorerank"], value["score"]])
    table = table.get_string(title=f"Round {round_number}")
    print(table)

def asking_end_of_day():
    """ Ask the user if the tournament is finish for the day
    Return : a bool """
    print("La journée est t'elle terminée ? y/n ")
    while True:
        answer = input("Réponse : ")
        if answer.lower() == 'y':
            return True
        elif answer.lower() == 'n':
            return False
        else:
            print("Merci de rentrer 'y' (oui) ou 'n' (non).")
""" View generated during the tournament """

def show_duel(list_of_duel):
    """ Print the list of duel """
    for player, index in zip(list_of_duel,range(len(list_of_duel))):
        print(f"{index+1}.{player[0]} affrontera {player[1]}.\n")


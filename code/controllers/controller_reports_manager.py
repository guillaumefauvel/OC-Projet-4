from models.player import Player
from datetime import datetime
from views.view_reports_manager import ask_for_report_choice
def reports_manager():
    ask_for_report_choice()
    pass

def make_players_dict():

    players_dict = {}

    sorted_registry = sorted(Player._registry, key=lambda x: x.reference, reverse=False)

    for player, index in zip(sorted_registry, range(1,len(Player._registry)+1)):
        players_dict[index] = [player.reference, player.ranking, player.birthday]

    return players_dict

def sort_by_rank():
    """ Use the player dict in order to etablish new rank
    Return : Another dict with a coherent indexes """

    sorted_by_rank = dict(sorted(make_players_dict().items(), key=lambda item: item[1][1]))

    for value, new_index in zip(sorted_by_rank, range(1,len(sorted_by_rank)+1)):
        sorted_by_rank[value][1] = new_index

    return sorted_by_rank

def sort_by_age():
    """ Use the birthday infos in the player dict in order to sort the player
    by their age.
    Return : A sorted dict with the name and the age of the player"""

    age_dict = {}

    for value in make_players_dict():
        raw_date = make_players_dict()[value][2]
        birthday = datetime.strptime(raw_date, '%d/%m/%Y').date()
        num_of_days = datetime.now().date() - birthday
        age_dict[value] = make_players_dict()[value][0],round(num_of_days.days/365)

    sorted_by_age = dict(sorted(age_dict.items(), key=lambda item: item[1][1]))

    return sorted_by_age

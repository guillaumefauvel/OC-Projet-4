from models.player import Player
from datetime import datetime
def make_players_dict():

    players_dict = {}

    for player, index in zip(Player._registry, range(1,len(Player._registry)+1)):
        players_dict[index] = [player.reference, player.ranking, player.birthday]

    return players_dict

def sort_by_rank():

    sorted_by_rank = dict(sorted(make_players_dict().items(), key=lambda item: item[1][1]))

    for value, new_index in zip(sorted_by_rank, range(1,len(sorted_by_rank)+1)):
        sorted_by_rank[value][1] = new_index

    for value in sorted_by_rank:
        print(sorted_by_rank[value])

    return sorted_by_rank

def sort_by_age():

    age_dict = {}

    for value in make_players_dict():
        raw_date = make_players_dict()[value][2]
        birthday = datetime.strptime(raw_date, '%d/%m/%Y').date()
        num_of_days = datetime.now().date() - birthday
        age_dict[value] = make_players_dict()[value][0],round(num_of_days.days/365)

    sorted_by_age = dict(sorted(age_dict.items(), key=lambda item: item[1][1]))

    return sorted_by_age
